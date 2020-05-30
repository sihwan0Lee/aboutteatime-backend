import jwt
from aboutteatime.settings import SECRET_KEY, HASH
from user.models import User

def logindecorator(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, algorithm = HASH)
                user_id = payload['id']
                user = User.objects.get(pk=user_id)
                request.user = user
            except jwt.DecodeError:
                return JsonResponse({'error':'INVALID_TOKEN'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'error':'NO_SUCH_USER'}, status=401)
            return func(welf, request, *args, **kwargs)
        else:
            return JsonResponse({'error':'LOGIN_REQUIRED'}, status=401)
    return wrapper
