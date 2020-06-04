import json

from django.utils import timezone
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Order, OrderStatus, OrderItem
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
            item_id      = data['item_id']
            delta        = data['delta']
            cur_item     = Item.objects.get(id=item_id)
            active_order = get_object_or_404(Order, user=user, status__status='active_cart')

            OrderItem.objects.filter(order=active_order, item=cur_item).update(quantity=F('quantity')+delta)
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error': 'INVALID_KEY'}, status=400)

    @logindecorator
    def get(self, request):
        user = request.user
        active_order = get_object_or_404(user.order_set, status__status='active_cart')
        print(active_order)
        items = active_order.items.all()
        print(items)
        bag_price = OrderItem.objects.aggregate(Sum('add_bag'))['add_bag__sum'] * 100
        cart_items = [
            {
                'id'            : item.id,
                'title'         : item.title,
                'price'         : int(item.price),
                'image'         : item.images.front_url,
                'benefits'      : item.get_benefits()[-1],
                'quantity'      : OrderItem.objects.get(order=active_order, item=item).quantity,
                'sub_total'     : int(item.price * OrderItem.objects.get(order=active_order, item=item).quantity),
                'discount'      : int(item.price * item.discount_percent)
            } for item in items
        ]
        discount = 0
        total = 0
        for item in cart_items:
            total += item['sub_total']
            discount += item['discount']
        shipping_cost = 0 if total > 30000 else 2500
        final_cost = total - discount
        num_items = len(items)

        summaries = {
            'discount'      : discount,
            'bag_price'     : bag_price,
            'total'         : total,
            'shipping_cost' : shipping_cost
        }
        return JsonResponse({'items': cart_items, 'summaries': summaries}, status=200)

    @logindecorator
    def delete(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            item_id = data['item_id']
            active_order = get_object_or_404(user.order_set, status__status='active_cart')
            OrderItem.objects.filter(order=active_order, item_id=item_id).delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status=400)

        

