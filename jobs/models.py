from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)


class Dokuman(models.Model):
    baslik = models.CharField(max_length=255)
    dosya = models.FileField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik
