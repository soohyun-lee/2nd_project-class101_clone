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

from user.models import User, Creator
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
    @decorator
    def get(self,request):
        product = Product.objects.get(creator_id=request.user)
        status = Product_Status.objects.prefetch_related('product').filter(product_id=product.id)
        introduction = Introduction.objects.filter(product_id=product.id)
        creator_intro = Creator.objects.get(user_id=request.user)
        creator_user = Creator.objects.get(user_id=request.user).id
        snslist = CreatorSNS.objects.filter(creator_id=creator_user)
        # id_number = 30
        # openclass = Product.objects.filter(id__gt = id_number)

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
            'hashtag'              : [tag.name for tag in Creator.objects.get(id=creator_user).hashtag_set.all()],
            "SNS": [{
                    "snsid"     : sns.sns_id,
                    "sns"       : sns.sns.name,
                    "account"   : sns.sns_account,
                    "address"   : sns.sns_address
                } for sns in snslist]}
                
        return JsonResponse({'data':open_product}, status=200)
