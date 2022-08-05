from django.contrib import admin

from django.contrib import admin
from .models import Invite, Client


admin.site.register(Invite)
admin.site.register(Client)
