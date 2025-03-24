from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="index"),
    path("care/", views.care, name="care"),
    path("care/care-add/", views.care_add, name="care-add"),
]
