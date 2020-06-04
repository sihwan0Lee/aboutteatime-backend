import json
import jwt
import bcrypt

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.utils.dateparse import parse_date


from aboutteatime.settings import SECRET_KEY, HASH
from user.models import User, UserGroup, CartCoupon, UserCartCoupon, Wishlist
from item.models import Item
from aboutteatime.utils import logindecorator

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            e_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                realname          = data['realname'],
                username          = data['username'],
                birthday          = data['birthday'],
                gender            = data['gender'],
                service_provider  = data['provider'],
                phone             = data['phone'],
                group             = UserGroup.objects.get(name='Green'),
                password          = e_password.decode('utf-8'),
                privacy_3rd_party = True if data.get('privacy_3rd_party') else False,
                privacy_foreign   = True if data.get('privacy_foreign') else False,
                point_message     = True if data.get('point_message') else False,
                web_message       = True if data.get('web_message') else False
            )
            new_user.save()
            UserCartCoupon.objects.create(user=new_user, coupon=CartCoupon.objects.get(name='온라인신규회원가입'), expiry_date='2120-1-1')
            return HttpResponse(status=200)
        except IntegrityError:
            return JsonResponse({'error':'EXISTING_VALUE'}, status=400)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(username = data['username']).exists():
                user = User.objects.get(username = data['username'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=HASH)
                    return JsonResponse({'token':token.decode('utf-8')}, status=200)
                return HttpResponse(status=401)
            return JsonResponse({'error':'INCORRECT_USERNAME'}, status=401)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status = 400)

class WishlistView(View):
    @logindecorator
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        try:
            is_addition = data['add']
            item_id = data['item_id']
            cur_item = Item.objects.get(id=item_id)
            if is_addition:
                Wishlist.objects.create(user=user, item=cur_item)
            else:
                Wishlist.objects.delete(user=user, item=cur_item)
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status=400)