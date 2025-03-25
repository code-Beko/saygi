from django.contrib.auth.models import AbstractUser
from django.db import models


# CustomUser modeli
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)


# Dokuman modeli
class Dokuman(models.Model):
    tersane = models.CharField(max_length=255)
    gemi = models.CharField(max_length=255)
    motor_ismi = models.CharField(max_length=255)
    is_no = models.CharField(max_length=255)
    musteri_ismi = models.CharField(max_length=255)
    tarih = models.DateField(default="2025-01-01")
    cihaz_teslim_alan = models.CharField(max_length=255)
    cihaz_turu = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    cihaz_markasi = models.CharField(max_length=255)
    seri_no = models.CharField(max_length=255)
    gucu = models.CharField(max_length=255)
    akim = models.CharField(max_length=255)
    voltaj = models.CharField(max_length=255)
    devir = models.CharField(max_length=255)
    ikaz_akimi = models.CharField(max_length=255)
    ikaz_voltaji = models.CharField(max_length=255)
    gelis_nedeni = models.CharField(max_length=255)
    parca = models.BooleanField(default=False)
    eksik_malzemeler = models.CharField(max_length=255)
    monte = models.BooleanField(default=False)
    demonte = models.BooleanField(default=False)
    kasnak_kaplin = models.BooleanField(default=False)
    fan_tasi = models.BooleanField(default=False)
    ayaklar = models.BooleanField(default=False)
    kama = models.BooleanField(default=False)
    klemens = models.BooleanField(default=False)
    fircalar = models.BooleanField(default=False)
    on_kapak = models.BooleanField(default=False)
    klemens_kapagi_kut = models.BooleanField(default=False)
    komurlar = models.BooleanField(default=False)
    arka_kapak = models.BooleanField(default=False)
    fan_pervane = models.BooleanField(default=False)
    rulmanlar = models.BooleanField(default=False)
    rulman_numarasi_on = models.CharField(max_length=255)
    rulman_numarasi_arka = models.CharField(max_length=255)
    demonte_eden = models.CharField(max_length=255)
    demonte_tarih = models.DateField(default="2025-01-01")
    saran_onaran = models.CharField(max_length=255)
    saran_onaran_tarih = models.DateField(default="2025-01-01")
    monte_eden = models.CharField(max_length=255)
    monte_eden_tarih = models.DateField(default="2025-01-01")
    test_eden = models.CharField(max_length=255)
    test_eden_tarih = models.DateField(default="2025-01-01")
    izolasyon_degerleri = models.CharField(max_length=25)
    calisma_akimi = models.CharField(max_length=255)
    calisma_gerilimi = models.CharField(max_length=255)
    diger_olcum_degerleri = models.CharField(max_length=255)
    test_cihazlari = models.CharField(max_length=255)
    yapilan_islemler = models.TextField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik
