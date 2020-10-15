import json
import jwt
import bcrypt
import boto3

from django.shortcuts  import render
from django.views      import View
from django.http       import JsonResponse
from datetime          import datetime
from django.db         import models
from .models           import (
    Product,
    DetailImage,
    Brand,
    Level,
    Introduction,
    Status,
    Product_Status
)

from user.models       import (User,
    Creator,
    SNS,
    Hashtag,
    CreatorSNS)

from decorator   import authorization
from django.core.files.storage import default_storage
# from urllib import parse


#전체 리스트
class Allproducts(View):
    def get(self,request):
        product_all = Product.objects.all()
        product_list = [{
            'id'               : product.id,
            'thumbnail'        : str(product.thumbnail),
            'category'         : product.category,
            'name'             : product.name,
            'heart_count'      : product.heart_count,
            'like'             : product.like,
            'retail_price'     : product.retail_price,
            'discount_percent' : product.discount_percent,
            'monthly_pay'      : product.monthly_pay,
            'monthly_payment'  : product.monthly_payment,
        } for product in product_all]

        return JsonResponse({'data':product_list}, status=200)
#MD추천
class RecommendView(View):
    def get(self,request):
        recommend_products = Product.objects.filter(like__gt = 92)
        recommend_product = [{
            'id'               : product.id,
            'thumbnail'        : str(product.thumbnail),
            'category'         : product.category,
            'name'             : product.name,
            'heart_count'      : product.heart_count,
            'like'             : product.like,
            'retail_price'     : product.retail_price,
            'discount_percent' : product.discount_percent,
            'monthly_pay'      : product.monthly_pay,
            'monthly_payment'  : product.monthly_payment,
        }for product in recommend_products]

        return JsonResponse({'data':recommend_product}, status=200)

#디테일 이미지 리스트
class Detailimage(View):
    def get(self,request):
        
        details = DetailImage.objects.select_related('product').all(product_id=1)
        detail_image = {
            'detail_image'     : [detail.detail_image for detail in details],
        }
        return JsonResponse({'data':detail_image}, status=200)



#디테일 우측 정보
class DetailView(View):
    def get(self,request):
        product = Product.objects.get(id=1)
        product_detail = {
            'id'               : product.id,
            'category'         : product.category,
            'name'             : product.name,
            'monthly_payment'  : product.monthly_payment,
            'monthly_pay'      : product.monthly_pay,
            'discount_percent' : product.discount_percent,
            'heart_count'      : product.heart_count,
            'end_datetime'     : product.end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return JsonResponse({'data':product_detail}, status=200)

# 디테일 recommend
class DetailView_Recommend(View):
    def get(self,request):
        like_count = 92
        recommend_products = Product.objects.filter(like__gt = like_count)
        recommend_product = [{
            'id'               : product.id,
            'thumbnail'        : str(product.thumbnail),
            'category'         : product.category,
            'name'             : product.name,
            'heart_count'      : product.heart_count,
            'like'             : product.like,
            'retail_price'     : product.retail_price,
            'discount_percent' : product.discount_percent,
            'monthly_pay'      : product.monthly_pay,
            'monthly_payment'  : product.monthly_payment,
        }for product in recommend_products]

        return JsonResponse({'data':recommend_product}, status=200)

# 오픈 예정
class OpenProduct(View):
    def get(self,request):
        openclass = Product.objects.filter(section_id = 2)
        open_product = [{
            'id'                   : product.id,
            'category'             : product.category,
            'thumbnail'            : str(product.thumbnail),
            'name'                 : product.name,
            'brand'                : product.brand_id,
            'detail_category'      : product.detail_category,
            'level'                : product.level_id,
            'cover_image'          : str(product.cover_image),
            'introduction_image'   :[str(intro.introduction_image) for intro in product.introduction_set.all()],
            'introduction_text'    :[intro_text.introduction_text for intro_text in product.introduction_set.all()],
            # 'status'               : [i.status_id for i in product.product_status_set.all()],
            'profile_image'        : product.creator.creator_set.all()[0].profile_image,
            'nickname'             : product.creator.creator_set.all()[0].nickname,
            'phone_number'         : product.creator.creator_set.all()[0].phone_number,
            'creator_introduction' : product.creator.creator_set.all()[0].creator_introduction,
            'hashtag'              : [tag.name for tag in product.creator.creator_set.first().hashtag_set.all()],
            'sns'                  : [{
                "snsid"     : sns.sns_id,
                "snsname"   : sns.sns.name,
                "account"   : sns.sns_account,
                "address"   : sns.sns_address
            }for sns in product.creator.creator_set.first().creatorsns_set.all()]
            } for product in openclass]

        return JsonResponse({'data':open_product}, status=200)

class BasicInformation(View):
    @authorization
    def post(self, request):
        data = json.loads(request.body)
        creator = request.user

        if Product.objects.filter(creator_id=creator).exists():
            Product.objects.filter(creator_id=creator).update(
            brand_id        = data['brand'],
            category        = data['category'],
            detail_category = data['detail_category'],
            level_id        = data['level'],
            )
            
        else:
            product = Product.objects.create(
            brand_id        = data['brand'],
            category        = data['category'],
            detail_category = data['detail_category'],
            level_id        = data['level'],
            creator_id      = creator
            )

            Product_Status.objects.create(
            product_id      = product.id,
            status_id       = 1
            )

        return JsonResponse({'data':'SUCCESS'}, status=200)

    @authorization
    def get(self,request):
        product = Product.objects.get(creator_id=request.user)
        status = Product_Status.objects.prefetch_related('product').filter(product_id=product.id)
        introduction = Introduction.objects.filter(product_id=product.id)
        creator_intro = Creator.objects.get(user_id=request.user)
        snslist = CreatorSNS.objects.filter(creator_id=creator_intro.id)

        open_product = {
            'id'                   : product.id,
            'category'             : product.category,
            'thumbnail'            : str(product.thumbnail),
            'name'                 : product.name,
            'retail_price'         : product.retail_price,
            'discount_percent'     : product.discount_percent,
            'monthly_pay'          : product.monthly_pay,
            'brand'                : product.brand_id,
            'detail_category'      : product.detail_category,
            'level'                : product.level_id,
            'cover_image'          : str(product.cover_image),
            'introduction_image'   : [str(image.introduction_image) for image in introduction],
            'introduction_text'    : [text.introduction_text for text in introduction],
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


class TitleAndCover(View):
    @authorization
    def post(self, request):
        # print(access_token)
        if Product.objects.filter(creator_id=request.user).exists():
        
            cover = request.FILES.get('cover')
            thumbnail = request.FILES.get('thumbnail')
            title = request.POST.get('title')
            default_storage.save(cover.name, cover)
            default_storage.save(thumbnail.name, thumbnail)

            return_cover_url = f"https://soohyunlee.s3.ap-northeast-2.amazonaws.com/static/{cover.name}"
            return_thumbnail_url = f"https://soohyunlee.s3.ap-northeast-2.amazonaws.com/static/{thumbnail.name}"
            
            Product.objects.filter(creator_id=request.user).update(
                    cover_image = return_cover_url,
                    thumbnail   = return_thumbnail_url,
                    name        = title
                    )

        else:
            product = Product.objects.create(
                cover_image = return_cover_url,
                thumbnail   = return_thumbnail_url,
                name        = title,
                creator_id  = request.user
                )

            Product_Status.objects.create(
                product_id      = product.id,
                status_id       = 2
                )
        
        return JsonResponse({'message':'SUCCESS'}, status=200) 

    @authorization
    def get(self,request):
        product = Product.objects.get(creator_id=request.user)
        status = Product_Status.objects.prefetch_related('product').filter(product_id=product.id)
        introduction = Introduction.objects.filter(product_id=product.id)
        creator_intro = Creator.objects.get(user_id=request.user)
        snslist = CreatorSNS.objects.filter(creator_id=creator_intro.id)

        open_product = {
            'id'                   : product.id,
            'category'             : product.category,
            'thumbnail'            : str(product.thumbnail),
            'name'                 : product.name,
            'retail_price'         : product.retail_price,
            'discount_percent'     : product.discount_percent,
            'monthly_pay'          : product.monthly_pay,
            'brand'                : product.brand_id,
            'detail_category'      : product.detail_category,
            'level'                : product.level_id,
            'cover_image'          : str(product.cover_image),
            'introduction_image'   : [str(image.introduction_image) for image in introduction],
            'introduction_text'    : [text.introduction_text for text in introduction],
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




class Introduce(View):
    @authorization
    def post(self, request):
        product = Product.objects.get(creator_id=request.user)
        introduction = Introduction.objects.filter(product_id=product.id)
        introduction.delete()

        introduction_images = request.FILES.getlist('introduction_image')
        introduction_text = request.POST.getlist('introduction_text')
        status = request.POST.get('status')
        
        n = Product_Status.objects.filter(product_id=product.id)
        url_list = []

        for i in introduction_images:
            default_storage.save(i.name, i)
            url_list.append(f"https://soohyunlee.s3.ap-northeast-2.amazonaws.com/static/{i.name}")

        ziplist = list(zip(url_list, introduction_text))

        for k in range(len(ziplist)):
            Introduction.objects.create(
                introduction_image = ziplist[k][0],
                introduction_text  = ziplist[k][1],
                product_id = Product.objects.get(creator_id=request.user).id
            )

        new = []
        for i in n:
            new.append(i.status_id)

        if int(status) not in new:
            Product_Status.objects.create(
            product_id      = product.id,
            status_id       = status
            )

        return JsonResponse({'message':'SUCCESS'}, status=200)

    @authorization
    def get(self,request):
        product = Product.objects.get(creator_id=request.user)
        status = Product_Status.objects.prefetch_related('product').filter(product_id=product.id)
        introduction = Introduction.objects.filter(product_id=product.id)
        creator_intro = Creator.objects.get(user_id=request.user)
        snslist = CreatorSNS.objects.filter(creator_id=creator_intro.id)

        open_product = {
            'id'                   : product.id,
            'category'             : product.category,
            'thumbnail'            : str(product.thumbnail),
            'name'                 : product.name,
            'retail_price'         : product.retail_price,
            'discount_percent'     : product.discount_percent,
            'monthly_pay'          : product.monthly_pay,
            'brand'                : product.brand_id,
            'detail_category'      : product.detail_category,
            'level'                : product.level.name,
            'cover_image'          : str(product.cover_image),
            'introduction_image'   : [str(image.introduction_image) for image in introduction],
            'introduction_text'    : [text.introduction_text for text in introduction],
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