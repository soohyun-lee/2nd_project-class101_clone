from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'brands'

class Level(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'levels'

class Product(models.Model):
    name             = models.CharField(max_length=45, null=True)
    category         = models.CharField(max_length=10, null=True)
    thumbnail        = models.ImageField(max_length=500, upload_to='usr', null=True)
    heart_count      = models.IntegerField(default=0, null=True)
    like             = models.IntegerField(default=0, null=True)
    retail_price     = models.FloatField(default=0, null=True)
    discount_percent = models.FloatField(default=0, null=True)
    monthly_pay      = models.FloatField(default=0, null=True)
    monthly_payment  = models.IntegerField(default=0, null=True)
    brand            = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    detail_category  = models.CharField(max_length=50, null=True)
    level            = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    cover_image      = models.ImageField(upload_to='usr', null=True)
    end_datetime     = models.DateTimeField(null=True)
    status           = models.ManyToManyField('Status', through='Product_Status', null=True)
#    creator          = models.ForeignKey(Creator, on_delete=models.CASCADE  유저앱 pull받은 뒤
    
    class Meta:
        db_table = 'products'

class DetailImage(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    detail_image = models.URLField(max_length=300, null=True)
    
    class Meta:
        db_table = 'detail_image'

class Introduction(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    introduction_image = models.ImageField(upload_to='usr', null=True)
    introduction_text  = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'introduction'

class Status(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'status'

class Product_Status(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    status  = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'product_status'
