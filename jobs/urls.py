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
    user_list,
    user_edit,
    user_delete,
)


urlpatterns = [
    path("", views.home, name="index"),
    path("care/", views.care, name="care"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/add/", views.task_add, name="task_add"),
    path("tasks/<int:id>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:id>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:id>/view/", views.task_view, name="task_view"),
    path("care/list/", document_list, name="document_list"),
    path("care/add/", document_add, name="document_add"),
    path("care/delete/<int:id>/", document_delete, name="document_delete"),
    path("document/<int:id>/edit/", views.document_edit, name="document_edit"),
    path("document-view/<int:id>/", views.document_view, name="document_view"),
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
    path("notifications/", notifications, name="notifications"),
    path("login/", login_view, name="login"),
    path("users/", user_list, name="user_list"),
    path("users/<int:id>/edit/", user_edit, name="user_edit"),
    path("users/<int:id>/delete/", user_delete, name="user_delete"),
]
#
