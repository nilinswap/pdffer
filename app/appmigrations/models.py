from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import datetime

class User(models.Model):
    class Meta:
            db_table = "users"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    aadhar_id = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=10)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    updated_on = models.DateTimeField(default=datetime.now, blank=True)


class ShopOwner(models.Model):
    class Meta:
            db_table = "shop_owners"

    id = models.BigAutoField(primary_key=True)
    pan_card_id = models.CharField(max_length=10)
    personal_address = models.TextField()
    user_details = models.ForeignKey(User, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

class ShopType(models.TextChoices):
        MEDICAL = 'MEDI', _('Medical')
        GROCERY = 'GROC', _('Grocery')
        HARDWARE = 'HDWR', _('Hardware')
        OTHERS = 'OTHR', _('OTHERS')

class Shop(models.Model):
    class Meta:
            db_table = "shops"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.FloatField()
    gst_number = models.CharField(max_length=50)
    type = models.CharField(
            max_length=4,
            choices=ShopType.choices,
            default=ShopType.OTHERS
    )
    owner = models.ForeignKey(ShopOwner, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

class Product(models.Model):
    class Meta:
            db_table = "products"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)


class Item(models.Model):
    class Meta:
            db_table = "items"

    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
