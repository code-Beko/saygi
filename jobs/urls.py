from django.urls import path
from . import views
from .views import dokuman_list, dokuman_ekle, dokuman_sil


urlpatterns = [
    path("", views.home, name="index"),
    path("care/", views.care, name="care"),
    path("care/list/", dokuman_list, name="dokuman_list"),
    path("care/add/", dokuman_ekle, name="dokuman_ekle"),
    path("care/delete/<int:id>/", dokuman_sil, name="dokuman_sil"),
    path("dokuman/<int:id>/duzenle/", views.dokuman_duzenle, name="dokuman_duzenle"),
]
