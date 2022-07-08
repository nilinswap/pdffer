from django.urls import path

from . import views

urlpatterns = [
    path('api/healthcheck/', views.healthcheck, name='healthcheck'),
    path('api/pdf/', views.get_pdf_from_html, name='pdf'),
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('please_verify_your_email', views.please_verify_your_email, name='please_verify_your_email'),
]
