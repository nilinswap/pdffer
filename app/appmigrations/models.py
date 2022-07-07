from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import datetime
import uuid
from encrypted_id.models import EncryptedIDModel

class Invite(models.Model):
    class Meta:
            db_table = "invite"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    

class Client(EncryptedIDModel):
    class Meta:
            db_table = "client"

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)
    invite = models.ForeignKey(Invite, on_delete=models.DO_NOTHING, null=True)
    last_logged_in = models.DateTimeField(default=datetime.now, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)


class ApiToken(models.Model):
    class Meta:
            db_table = "api_token"

    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=500, unique=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)


# class Session(models.Model):
#     class Meta:
#             db_table = "session"

#     id = models.BigAutoField(primary_key=True)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     session_id = models.CharField(max_length=500, unique=True)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now=True)
