
import json
from django.test import TestCase, Client

from user.models import User
from .models     import (
    Product,
    DetailImage,
    Brand,
    Level,
    Introduction,
    Status,
    Product_Status
)

client = Client()
class AllproductsTest(TestCase):
    def setUp(self):
        Product.objects.create(
            id               = 1,
            category         = '여행',
            name             = '여행을 떠나는 클래스',
            thumbnail        = "https://soohyunlee.s3.ap-northeast-2.amazonaws.com/kim.jpg",
            heart_count      = 100,
            like             = 900000,
            retail_price     = 900000.0,
            discount_percent = 50,
            monthly_pay      = 5,
            monthly_payment  = 10000,
        )
    def tearDown(self):
        Product.objects.all().delete()

    def test_allproduct_get_success(self):
        client = Client()

        response = client.get('/products')
        self.assertEqual(response.json(),
            {
            "data": [{
            "id": 1,
            "category": "여행",
            "name": "여행을 떠나는 클래스",
            "thumbnail" : "https://soohyunlee.s3.ap-northeast-2.amazonaws.com/kim.jpg",
            "heart_count": 100,
            "like": 900000,
            "retail_price" : 900000.0,
            "discount_percent": 50.0,
            "monthly_pay": 5.0,
            "monthly_payment": 10000
        }]
            }
        )
        self.assertEqual(response.status_code, 200)


class RecommendViewTest(TestCase):
    def setUp(self):
        Product.objects.create(
            id               = 2,
            category         = '여행',
            name             = '여행을 떠나는 클래스',
            thumbnail        = "https://soohyunlee.s3.ap-northeast-2.amazonaws.com/kim.jpg",
            heart_count      = 100,
            like             = 95,
            retail_price     = 900000.0,
            discount_percent = 50.0,
            monthly_pay      = 5.0,
            monthly_payment  = 10000,
        )
        Product.objects.create(
            id               = 3,
            category         = '여행',
            name             = '여행을 떠나는 클래스',
            thumbnail        = "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60",
            heart_count      = 100,
            like             = 90,
            retail_price     = 900000.0,
            discount_percent = 50.0,
            monthly_pay      = 5.0,
            monthly_payment  = 10000,
        )

    def tearDown(self):
        Product.objects.all().delete()

    def test_recommend_get_success(self):
        client = Client()

        response = client.get('/products/recommend')
        self.assertEqual(response.json(),
            {
            "data": [{
            "id": 2,
            "category": "여행",
            "name": "여행을 떠나는 클래스",
            "thumbnail" : "https://soohyunlee.s3.ap-northeast-2.amazonaws.com/kim.jpg",
            "heart_count": 100,
            "like": 95,
            "retail_price" : 900000.0,
            "discount_percent": 50.0,
            "monthly_pay": 5.0,
            "monthly_payment": 10000
        }]
            }
        )
        self.assertEqual(response.status_code, 200)