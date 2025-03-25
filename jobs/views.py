from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Dokuman
from .forms import DokumanForm
from datetime import datetime
from django.core.paginator import Paginator


def home(request):
    return render(request, "index.html")


def care(request):
    return render(request, "care.html")


def dokuman_list(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    dokumanlar = Dokuman.objects.all().order_by('-created_at')  # created_at'a göre azalan sırayla

    if query:
        dokumanlar = dokumanlar.filter(
            Q(tersane__icontains=query)
            | Q(gemi__icontains=query)
            | Q(motor_ismi__icontains=query)
        )

    # Tarih filtresi
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            dokumanlar = dokumanlar.filter(tarih__range=[start_date, end_date])
        except ValueError:
            pass  # Geçersiz tarih girilirse hata oluşmaması için

    # Sayfalama (her sayfada 50 doküman)
    paginator = Paginator(dokumanlar, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "care/list.html",
        {
            "dokumanlar": page_obj,  # Sayfalanmış nesneleri gönderiyoruz
            "query": query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )



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
