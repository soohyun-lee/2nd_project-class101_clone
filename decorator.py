import json
import jwt
from django.views    import View
from django.http     import JsonResponse
from user.models         import User
from ilnass.settings     import SECRET_KEY, ALGORITHM
def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)      
            if access_token:
                token_paylod    = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                request.user = User.objects.get(email = token_paylod['email']).id
                return func(self, request, *args, **kwargs)
            return JsonResponse({'MESSAGE':'LOGIN_REQUIRED'}, status = 401)
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_USER1'}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER2'}, status = 401)
    return wrapper