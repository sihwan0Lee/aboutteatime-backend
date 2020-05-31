import json
import jwt
import bcrypt

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from aboutteatime.settings import SECRET_KEY, HASH
from user.models import User, UserGroup, CartCoupon

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            b_password = data['password'].encode('utf-8')  
            new_user = User(
                realname          = data['realname'],
                username          = data['username'],
                birthday          = data['birthday'],
                gender            = data['gender'],
                service_provider  = data['provider'],
                phone             = data['phone'],
                group             = UserGroup.objects.get(name='Green'),
                password          = bcrypt.hashpw(b_password, bcrypt.gensalt()),
                privacy_3rd_party = True if data.get('privacy_3rd_party') else False,
                privacy_foreign   = True if data.get('privacy_foreign') else False,
                point_message     = True if data.get('point_message') else False,
                web_message       = True if data.get('web_message') else False
            }
            new_user.save()
            new_user.cart_coupons.add(CartCoupon.objects.get(name='온라인신규회원가입'))
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
                if bcrypt.checkpw(data['password'].encode(‘utf-8’), user.password.encode(‘utf-8’)):
                    token = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=HASH)
                    return JsonResponse({'token':token.decode('utf-8')}, status=200)
                return HttpResponse(status=401)
            return JsonResponse({'error':'INCORRECT_USERNAME'}, status=401)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status = 400)
