from django.urls import path

from . import views

urlpatterns = [
    path("a", views.a, name="a"),
    path("", views.index, name="index"),
    path("api/healthcheck/", views.healthcheck, name="healthcheck"),
    path("api/pdf/", views.get_pdf_from_html, name="pdf"),
]
