import json

from django.utils import timezone
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db import transaction, IntegrityError

from .models import Order, OrderStatus, OrderItem, PaymentMethod
from user.models import User
from item.models import Item
from aboutteatime.utils import logindecorator

class CartView(View):
    @logindecorator
    def post(self, request):
        try:
            user        = request.user
            data        = json.loads(request.body)
            item_id     = data['item_id']
            quantity    = data['quantity']
            add_bag     = data['add_bag']
            num_bags = 0
            if add_bag:
                num_bags = quantity
            cur_item = Item.objects.get(id=item_id)

            if Order.objects.filter(user=user, status__status='active_cart').exists():
                active_order = Order.objects.get(user=user, status__status='active_cart')
            else:
                active_order = Order(user=user, status=OrderStatus.objects.get(status='active_cart'))
                active_order.save()

            if OrderItem.objects.filter(order=active_order, item=cur_item).exists():
                OrderItem.objects.filter(order=active_order, item=cur_item).update(quantity=F('quantity')+quantity, add_bag=F('add_bag')+num_bags)
            else:
                OrderItem.objects.create(order=active_order, item=cur_item, quantity=quantity, add_bag=num_bags)

            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error': 'INVALID_KEY'}, status=400)

    @logindecorator
    def patch(self, request):
        try:
            user         = request.user
            data         = json.loads(request.body)
            orderitem_id = data['cart_id']
            delta        = data['delta']
            
            if delta < 0 and OrderItem.objects.get(id=orderitem_id).quantity == 1:
                return HttpResponse(status=400)
            OrderItem.objects.filter(id=orderitem_id).update(quantity=F('quantity')+delta)
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error': 'INVALID_KEY'}, status=400)

    @logindecorator
    def get(self, request):
        user = request.user
        active_order = user.order_set.filter(status__status='active_cart').first()
        if not active_order:
            active_order = Order(user=user, status=OrderStatus.objects.get(status='active_cart'))
            active_order.save()
        items = active_order.items.all()
        num_bags = OrderItem.objects.filter(order=active_order).aggregate(Sum('add_bag'))['add_bag__sum'] 
        bag_price = num_bags * 100 if num_bags != None else 0
        cart_items = [
            {
                'id'            : item.id,
                'cart_id'       : OrderItem.objects.get(order=active_order, item=item).id, 
                'title'         : item.title,
                'price'         : int(item.price),
                'image'         : item.images.front_url,
                'benefits'      : item.get_benefits()[-1],
                'quantity'      : OrderItem.objects.get(order=active_order, item=item).quantity,
                'sub_total'     : int(item.price * OrderItem.objects.get(order=active_order, item=item).quantity),
                'discount'      : 0 if item.discount_percent == 1 else int(item.price * item.discount_percent)
            } for item in items
        ]
        discount = 0
        total = 0
        for item in cart_items:
            total += item['sub_total']
            discount += item['discount']
        shipping_cost = 0 if total > 30000 or total == 0 else 2500
        final_cost = total - discount + shipping_cost + bag_price
        num_items = len(items)

        summaries = {
            'discount'      : discount,
            'bag_price'     : bag_price,
            'total'         : total,
            'shipping_cost' : shipping_cost,
            'final_cost'    : final_cost,
            'num_items'     : num_items
        }
        return JsonResponse({'items': cart_items, 'summaries': summaries}, status=200)

    @logindecorator
    def delete(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            orderitem_id = data['cart_id']
            OrderItem.objects.filter(id=orderitem_id).delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status=400)

class OrderView(View):
    @logindecorator
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            orderitem_ids      = data['orderitem_ids']
            payment_method     = data['payment_method']
            request_message    = data['request_message']
            total_price        = data['total_price']
            final_price        = data['final_price']
            shipping_fee       = data['shipping_fee']
            cash_receipt_phone = data.get('cash_receipt_phone', None)
            escrow_policy      = data.get('escrow_policy', False)
            
            with transaction.atomic():
                cur_order = user.order_set.filter(status__status='active_cart').first()
                if len(orderitem_ids) == len(cur_order.orderitem_set.all()):
                    cur_order.status = OrderStatus.objects.get(status='order_placed')
                    cur_order.save()
                    order_placed = cur_order
                    Order.objects.create(user=user, status=OrderStatus.objects.get(status='active_cart'))
                else:
                    new_order = Order(user=user, status=OrderStatus.objects.get(status='order_placed'))
                    new_order.save()
                    order_placed = new_order
                    for each_id in orderitem_ids:
                        OrderItem.objects.filter(id=each_id).update(order=new_order)
                
                order_placed.payment_method     = PaymentMethod.objects.get(method=payment_method)
                order_placed.request_message    = request_message
                order_placed.total_price        = total_price
                order_placed.final_price        = final_price
                order_placed.shipping_fee       = shipping_fee
                order_placed.cash_receipt_phone = cash_receipt_phone if cash_receipt_phone else None
                order_placed.escrow_policy      = escrow_policy if escrow_policy else False
                order_placed.ordered_date       = timezone.now()
                order_placed.save()
                return HttpResponse(status=200)
        except IntegrityError:    
            return JsonResponse({'error':'TRANSACTION_FAILURE'}, status=400)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status=400)

    @logindecorator
    def get(self, request):
        user = request.user
        cart_ids = request.GET.get('ids').split(",")
        cart = OrderItem.objects.filter(id__in=cart_ids)
        items = [
            {
                'id'        : order_item.item.id,
                'title'     : order_item.item.title,
                'price'     : float(order_item.item.price),
                'quantity'  : order_item.quantity,
                'bag_price' : order_item.add_bag * 100,
                'sub_total' : order_item.quantity * float(order_item.item.price)
            } for order_item in cart
        ] 
        cart_coupon_values = user.cart_coupons.values_list('name', 'discount', 'min_order')
        cart_coupons = [
            {
                'name'      : values[0],
                'discount'  : values[1],
                'min_order' : float(values[2])
            } for values in cart_coupon_values
        ]
        mobile_coupon_values = user.mobile_coupons.values_list('name', 'serial_number', 'expiry_date')
        mobile_coupons = [
            {
                'name'           : values[0],
                'serial_number'  : values[1],
                'expiry_date'    : values[2]
            } for values in mobile_coupon_values
        ]
        user_info = {
            'realname'  : user.realname,
            'phone'     : user.phone
        }
        user_addresses = user.address_set.values_list('address_name', 'recipient_name', 'address', 'phone')
        addresses = [
            {
                'address_name'      : address[0],
                'recipient_name'    : address[1],
                'address'           : address[2],
                'phone'             : address[3]
            } for address in user_addresses
        ]
        total = 0
        bag_price = 0
        for item in items:
            total += item['sub_total']
            bag_price += item['bag_price']
        shipping = 0 if total > 30000 else 2500
        final_cost = total + bag_price + shipping
        summaries = {
            'total'     : total,
            'bag_price' : bag_price,
            'shipping'  : shipping,
            'final_cost': final_cost
        }

        return JsonResponse({
            'items'         : items, 
            'cart_coupons'  : cart_coupons, 
            'mobile_coupons': mobile_coupons,
            'user_info'     : user_info,
            'user_addresses': addresses,
            'summaries'     : summaries
            }, status=200)
