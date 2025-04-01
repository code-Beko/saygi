from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Document


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "department", "yetki", "is_staff", "is_active")
    list_filter = ("department", "yetki", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Kişisel Bilgiler",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "İzinler",
            {
                "fields": (
                    "department",
                    "yetki",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Önemli Tarihler", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "department",
                    "yetki",
                ),
            },
        ),
    )
    search_fields = ("username", "email", "department")
    ordering = ("username",)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("shipyard", "boat", "engine_name", "date", "created_at")
    list_filter = ("shipyard", "boat", "date")
    search_fields = ("shipyard", "boat", "engine_name")
    ordering = ("-created_at",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Document, DocumentAdmin)
