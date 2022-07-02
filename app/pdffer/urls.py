from django.urls import path

from . import views

urlpatterns = [
    path('api/find-shops/', views.find_shops_on_product, name='find-shops'),
    path('api/items-in-shop/', views.find_items_in_shop, name='items-in-shop'),
    path('api/healthcheck/', views.healthcheck, name='healthcheck'),
    path('', views.index, name='index'),
]