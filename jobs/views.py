from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def care(request):
    return render(request, "care.html")


def care_add(request):
    return render(request, "care/care_add.html")
