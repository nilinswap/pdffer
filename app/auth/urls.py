from django.urls import path

from . import views

urlpatterns = [
    path('token/create', views.create_token, name='create_token'),
    # path('token/verify/<slug:api_key>', views.verify_token, name='verify_token'),
]