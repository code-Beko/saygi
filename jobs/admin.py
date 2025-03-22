from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _


# Grupları oluşturacak fonksiyon
def create_groups():
    # Kurucu Grubu
    founder_group, created = Group.objects.get_or_create(name="Kurucu")
    if created:
        founder_group.permissions.set(Permission.objects.all())

    # Müdür Grubu
    manager_group, created = Group.objects.get_or_create(name="Müdür")
    if created:
        manager_group.permissions.set(
            Permission.objects.filter(codename__contains="manage")
        )

    # Departman Müdürü Grubu
    department_head_group, created = Group.objects.get_or_create(
        name="Departman Müdürü"
    )
    if created:
        department_head_group.permissions.set(
            Permission.objects.filter(codename__contains="manage_department")
        )

    # Çalışan Grubu
    employee_group, created = Group.objects.get_or_create(name="Çalışan")
    if created:
        employee_group.permissions.set(
            Permission.objects.filter(codename__contains="view")
        )
