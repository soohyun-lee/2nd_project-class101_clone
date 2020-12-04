import bcrypt, json, jwt, re, requests
from django.http      import HttpResponse, JsonResponse
from django.views     import View
from ilnass.settings  import SECRET_KEY, ALGORITHM
from user.models      import (User,
                             Creator,
                             SNS,
                             CreatorSNS,
                             Hashtag)
from product.models   import (Product, 
                             Product_Status, 
                             Status,
                             Brand,
                             Level,
                             Section,
                             Product,
                             Introduction
                             )
from decorator        import authorization
class KakaoSignIn(View):
    def post(self, request):
        try:
            token        = request.headers.get('Authorization')
            profile_json = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'}).json()
            print(profile_json)
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
                sns     = data['sns'][i]['sns']
                sns1    = data['sns'][i]['account']
                sns2    = data['sns'][i]['address']
                # if data['photo'] == '' or data['nickname'] == '' or data['phone_no'] == '' or data['personality'] == '':
                #     return JsonResponse({'message':'blank is not allowed'}, status=401)
                # else:
                
                creator = Creator.objects.get(user_id = request.user)
                Creator.objects.filter(user_id = request.user).update(
                    # user                 = User.objects.get(id=request.user),
                    profile_image        = data['photo'],
                    nickname             = data['nickname'],
                    phone_number         = data['phone_no'],
                    creator_introduction = data['personality'],
                )

                CreatorSNS.objects.create(
                    sns_account = sns1,
                    sns_address = sns2,
                    creator_id  = creator.id,
                    sns_id      = SNS.objects.get(name=sns).id
                )

                Hashtag.objects.create(
                    name       = data['hashtag'],
                    creator_id = creator.id
                )

                Product_Status.objects.create(
                    product_id = Product.objects.get(creator_id = request.user).id, 
                    status_id   = 4
                )

                return JsonResponse({'message':'SUCCESS'}, status=200)   
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=430)
        except Creator.DoesNotExist:
            return JsonResponse({'message':'Such sns does not exist.'})


    @authorization
    def get(self,request):
        product = Product.objects.get(creator_id=request.user)
        status = Product_Status.objects.prefetch_related('product').filter(product_id=product.id)
        introduce = Introduction.objects.filter(product_id=product.id)
        creator_intro = Creator.objects.get(user_id=request.user)
        snslist = CreatorSNS.objects.filter(creator_id=creator_intro.id)
        open_product = {
            'id'                   : product.id,
            'category'             : product.category,
            'thumbnail'            : str(product.thumbnail),
            'name'                 : product.name,
            'brand'                : product.brand_id,
            'detail_category'      : product.detail_category,
            'level'                : product.level_id,
            'cover_image'          : str(product.cover_image),
            'introduction_image'   : [str(image.introduction_image) for image in introduce],
            'introduction_text'    : [text.introduction_text for text in introduce],
            'status'               : [i.status.name for i in Product_Status.objects.prefetch_related('product').filter(product_id=product.id)],
            'profile_image'        : creator_intro.profile_image,
            'nickname'             : creator_intro.nickname,
            'phone_number'         : creator_intro.phone_number,
            'creator_introduction' : creator_intro.creator_introduction,
            'hashtag'              : [tag.name for tag in Creator.objects.get(id=creator_intro.id).hashtag_set.all()],
            "SNS": [{
                    "snsid"     : sns.sns_id,
                    "sns"       : sns.sns.name,
                    "account"   : sns.sns_account,
                    "address"   : sns.sns_address
                } for sns in snslist]}
        return JsonResponse({'data':open_product}, status=200)