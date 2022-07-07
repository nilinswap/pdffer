from django.urls import path

from . import views

urlpatterns = [
    path('api/healthcheck/', views.healthcheck, name='healthcheck'),
    path('api/pdf/', views.get_pdf_from_html, name='pdf'),
    path('', views.index, name='index'),
]