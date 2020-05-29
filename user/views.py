import json
import jwt
import bcrypt

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.db.models import Q

from aboutteatime.utils import logindecorator
from aboutteatime.settings import SECRET, HASH
from user.models import User, UserStatus

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            b_password = data['password'].encode('utf-8')  
            User.objects.create(
                realname          = data['realname'],
                username          = data['username'],
                birthday          = data['birthday'],
                gender            = data['gender'],
                service_provider  = data['provider'],
                phone             = data['phone'],
                group             = UserGroup.objects.get(pk=1),
                password          = bcrypt.hashpw(b_password, bcrypt.gensalt()),
                privacy_3rd_party = data['privacy_3rd_party'] if data.get('privacy_3rd_party') else False,
                privacy_foreign   = data['privacy_foreign'] if data.get('privacy_foreign') else False,
                point_message     = data['point_message'] if data.get('point_message') else False,
                web_message       = data['web_message'] if data.get('web_message') else False
            }
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
                    token = jwt.encode({'user_id':user.id}, SECRET, algorithm=HASH)
                    return JsonResponse({'token':token.decode('utf-8')}, status=200)
            return JsonResponse({'error':'INCORRECT_ID_OR_PASSWORD'}, status=400)
        except KeyError:
            return JsonResponse({'error':'INVALID_KEY'}, status = 400)
