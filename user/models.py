from django.db import models
class User(models.Model):
    email        = models.CharField(max_length = 50, null=True)
    password     = models.IntegerField(default = 0, null=True) 
    phone_number = models.CharField(max_length = 50, null=True)
    name         = models.CharField(max_length = 50, null=True)
    nickname     = models.CharField(max_length = 50, null=True)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

class SNS(models.Model):
    name    = models.CharField(max_length = 50, null=True)

    class Meta:
        db_table = 'sns'        

class Creator(models.Model):
    user                 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile_image        = models.URLField(null=True)
    nickname             = models.CharField(max_length = 50, null=True)
    phone_number         = models.CharField(max_length = 50, null=True)
    creator_introduction = models.TextField(null=True)
    sns_name             = models.ManyToManyField(SNS, through = 'CreatorSNS')
    created_at           = models.DateTimeField(auto_now_add = True)
    updated_at           = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'creator'

class Hashtag(models.Model):
    name    = models.CharField(max_length = 50, null=True)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'hashtag'

class CreatorSNS(models.Model):
    creator      = models.ForeignKey(Creator, on_delete = models.CASCADE, null=True)
    sns          = models.ForeignKey(SNS, on_delete = models.CASCADE, null=True)
    sns_account  = models.CharField(max_length = 50, null = True)
    sns_address  = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'creator_sns'
