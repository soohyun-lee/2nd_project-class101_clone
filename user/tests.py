class CreatorIntroTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email        = "something",
            password     = 12345678,
            phone_number = "something",
            name         = "something",
            nickname     = "something",
            id = 1
        )
        SNS.objects.create(
            name = "facebook",
            id = 1
        )
        Creator.objects.create(
            user_id              = 1,
            profile_image        = 'randomvalueblahblah',
            nickname             = 'somebody',
            phone_number         = '12345678',
            creator_introduction = 'blahblah',
            id = 1
        )
        Hashtag.objects.create(
            name       = 'randomthing',
            creator_id = 1,
            id = 1
        )
        CreatorSNS.objects.create(
            creator_id  = 1,
            sns_id      = 1,
            sns_account = 'sungjinny',
            sns_address = 'something@facebook.com',
            id = 1
        )
        Product.objects.create(
            name = 'somethingexists'
        )
        Status.objects.create(name = 'done', id = 1)
        Status.objects.create(name = 'lit', id = 2)
        Status.objects.create(name = 'legit', id = 3)
        Status.objects.create(name = 'dope', id = 4)
        Product_Status.objects.create(
            product_id = 1,
            status_id  = 4,  
            id = 1
        )
    def tearDown(self):
        User.objects.all().delete()
        SNS.objects.all().delete()
        Creator.objects.all().delete()
        Hashtag.objects.all().delete()
        CreatorSNS.objects.all().delete()
        Product.objects.all().delete()
    @patch('user.views.requests')
    def test_creatorintro_post_success(self):
        client = Client()
        creator = {
            'user'                 : User.objects.get(id=1),
            'profile_image'        : 'randomvalueblahblah',
            'nickname'             : 'somebody',
            'phone_number'         : '12345678',
            'creator_introduction' : 'blahblah'
        }
        creator_sns = {
            'sns_account' : 'sungjinny',
            'sns_address' : 'something@facebook.com',
            'creator_id'     : 1,
            'sns_id'      : 1
        }
        hashtag = {
            'name'    : 'randomthing',
            'creator_id' : 1
        }
        product_status = {
            'product_id' : 1,
            'status_id'  : 4
        }
        response = client.post('/user/creator/intro', json.dumps(creator, creator_sns, hashtag, product_status), {'content_type':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message': 'welldone'
            }
        )