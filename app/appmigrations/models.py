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


class Client(models.Model):
    class Meta:
            db_table = "client"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)


class ApiToken(models.Model):
    class Meta:
            db_table = "api_token"

    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=500, unique=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
