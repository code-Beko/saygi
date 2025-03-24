from django.shortcuts import render, redirect
from .models import Dokuman
from .forms import DokumanForm


def home(request):
    return render(request, "index.html")


def care(request):
    return render(request, "care.html")


def dokuman_list(request):
    dokumanlar = Dokuman.objects.all()
    return render(request, "care/list.html", {"dokumanlar": dokumanlar})


def dokuman_ekle(request):
    if request.method == "POST":
        form = DokumanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dokuman_list")
    else:
        form = DokumanForm()
    return render(request, "care/add.html", {"form": form})


def dokuman_sil(request, id):
    dokuman = Dokuman.objects.get(id=id)
    dokuman.delete()
    return redirect("dokuman_list")
