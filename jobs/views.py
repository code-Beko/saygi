from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test


def is_manager(user):
    return user.groups.filter(name="Müdür").exists()


@user_passes_test(is_manager)
def manager_view(request):
    return render(request, "manager_dashboard.html")


def home(request):
    return render(request, "index.html")
