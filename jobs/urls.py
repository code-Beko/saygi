from django.urls import path
from . import views
from .views import (
    document_list,
    document_add,
    document_delete,
    signup,
    profile,
    notifications,
    login_view,
)


urlpatterns = [
    path("", views.home, name="index"),
    path("care/", views.care, name="care"),
    path("care/list/", document_list, name="document_list"),
    path("care/add/", document_add, name="document_add"),
    path("care/delete/<int:id>/", document_delete, name="document_delete"),
    path("document/<int:id>/edit/", views.document_edit, name="document_edit"),
    path("document-view/<int:id>/", views.document_view, name="document_view"),
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
    path("notifications/", notifications, name="notifications"),
    path("login/", login_view, name="login"),
]
#
