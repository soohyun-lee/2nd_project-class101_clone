import bcrypt, json, jwt, re, requests

from django.shortcuts import render
from django.http      import HttpResponse, JsonResponse
from django.views     import View
from my_settings      import SECRET_KEY, ALGORITHM
from .models          import (User,
                            Creator,
                            SNS,
                            CreatorSNS)

from product.models   import (Product,
                            DetailImage,
                            Brand,
                            Level,
                            Introduction,
                            Status,
                            Product_Status
                            )
from decorator import authorization


class KakaoSignIn(View):
    def post(self, request):
        try:
            token        = request.headers.get('Authorization')
            profile_json = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'}).json()

            data_kakao = profile_json['kakao_account']
            email    = data_kakao['email']
            nickname = data_kakao['profile']['nickname']

            if User.objects.filter(email = email).exists():
                user = User.objects.get(email = email)

            else:
                User.objects.create(
                    email    = email,
                    nickname = nickname
                )

            access_token = jwt.encode({'email':email}, SECRET_KEY, algorithm = ALGORITHM)
            access_token = access_token.decode("utf-8")

            return JsonResponse({'access_token':access_token}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 402)

        