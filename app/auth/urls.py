from django.urls import path

from . import views

urlpatterns = [
    path('invite/verify', views.verify_invite, name='verify_invite'),
    path('client/create', views.create_client, name='create_client'),
    # path('token/verify/<slug:api_key>', views.verify_token, name='verify_token'),
]