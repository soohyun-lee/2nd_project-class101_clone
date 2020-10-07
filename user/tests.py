import json

import bcrypt, re, requests

from .models        import User, SNS, Creator, CreatorSNS
from django.test    import TestCase
from django.test    import Client
from unittest.mock  import patch, MagicMock

class KakaoSignInTest(TestCase):

    def setUp(self):
        User.objects.create(
            email    = 'email',
            nickname = 'someonethx'
        )
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch('user.views.requests') # user앱의 views.py에서 사용될 requests patch
    def test_kakaosignin_post_success(self, mocked_requests):
        client = Client()

        class MockResponse:
            def json(self):
                return{
                    "kakao_account":{
                    'email'   : 'email',
                    'profile' : {'nickname':'someonethx'}
                }
                }
        mocked_requests.get = MagicMock(return_value = MockResponse())

        user = {
            'email'   : 'something@gmail.com',
            'profile' : {'nickname' : 'someonethx'}
        }
        response = client.post('/user/signin/kakao/callback', json.dumps(user), **{'Authorization':'1234', 'content_type':'application/json'})
        #response = client.post('/user/signin/kakao/callback', **{'Authorization':'1234', 'content_type':'application/json'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImVtYWlsIn0.MY5vOH0OUeQI3YMRyIxYeMf3h-ekDhO_lz7LSRjIoGc'

            }
        )

class CreatorIntroTest(TestCase):

    def setUp(self):
        Creator.objects.create(
            user                 = request.user.id,
            profile_image        = 'something.jpg',
            nickname             = 'somebody',
            phone_number         = '1234567',
            sns_name             = 'facebook',
            creator_introduction = 'blahblah'
        )
        CreatorSNS.objects.create(
            sns_account = 'sungjinny',
            sns_address = 'something@facebook.com'
        )
    
    def tearDown(self):
        Creator.objects.all().delete()