from django.urls import path

from . import views

urlpatterns = [
    path('invite/verify', views.verify_invite, name='verify_invite'),
    path('client/create/', views.create_client, name='create_client'),
    path('client/delete', views.delete_client, name='delete_client'),
    path('verify_email/<slug:link_ekey>', views.verify_email, name='verify_email'),
    path('verify_login/', views.verify_login, name='verify_login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    # path('token/verify/<slug:api_key>', views.verify_token, name='verify_token'),
]