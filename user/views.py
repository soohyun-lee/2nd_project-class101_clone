import bcrypt, json, jwt, re, requests
from django.http      import HttpResponse, JsonResponse
from django.views     import View
from ilnass.settings  import SECRET_KEY, ALGORITHM
from user.models      import (User,
                             Creator,
                             SNS,
                             CreatorSNS,
                             Hashtag)
from product.models   import Product, Product_Status
from decorator        import authorization
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
class CreatorIntro(View):
    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            for i in range(0,100):
                sns     = data['sns'][i]['channel']
                sns1    = data['sns'][i]['channel_id']
                sns2    = data['sns'][i]['channel_url']
                if data['photo'] == '' or data['nickname'] == '' or data['phone_no'] == '' or data['personality'] == '':
                    return JsonResponse({'message':'blank is not allowed'}, status=401)
                else:
                    new_creator = Creator.objects.create(
                        user                 = User.objects.get(id=request.user),
                        profile_image        = data['photo'],
                        nickname             = data['nickname'],
                        phone_number         = data['phone_no'],
                        creator_introduction = data['personality'],
                    )
                    CreatorSNS.objects.create(
                        sns_account = sns1,
                        sns_address = sns2,
                        creator     = new_creator,
                        sns_id      = SNS.objects.get(name=sns).id
                    )
                    Hashtag.objects.create(
                        name    = data['hashtag'],
                        creator = new_creator
                    )
                    Product_Status.objects.create(
                        prodcuct_id = Product.objects.get(creator_id=request.user).id,
                        status      = 4
                    )
                return JsonResponse({'message':'SUCCESS'}, status=200)   
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=430)
        except Creator.DoesNotExist:
            return JsonResponse({'message':'Such sns does not exist.'})