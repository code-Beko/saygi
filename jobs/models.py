from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _


# CustomUser modeli
class CustomUser(AbstractUser):
    phone_number = models.CharField(_("Telefon Numarası"), max_length=15, blank=True, null=True)
    department = models.CharField(_("Departman"), max_length=100, blank=True, null=True)


# Dokuman modeli
class Dokuman(models.Model):
    tersane = models.CharField(_("Tersane"), max_length=255, null=True, blank=True)
    gemi = models.CharField(_("Gemi"), max_length=255, null=True, blank=True)
    motor_ismi = models.CharField(_("Motor İsmi"), max_length=255, null=True, blank=True)
    is_no = models.CharField(_("İş No"), max_length=255, null=True, blank=True)
    musteri_ismi = models.CharField(_("Müşteri İsmi"), max_length=255, null=True, blank=True)
    tarih = models.DateField(_("Tarih"), null=True, blank=True, default=date.today)
    cihaz_teslim_alan = models.CharField(_("Cihaz Teslim Alan"), max_length=255, null=True, blank=True)
    cihaz_turu = models.CharField(_("Cihaz Türü"), max_length=255, null=True, blank=True)
    model = models.CharField(_("Model"), max_length=255, null=True, blank=True)
    cihaz_markasi = models.CharField(_("Cihaz Markası"), max_length=255, null=True, blank=True)
    seri_no = models.CharField(_("Seri No"), max_length=255, null=True, blank=True)
    gucu = models.CharField(_("Gücü"), max_length=255, null=True, blank=True)
    akim = models.CharField(_("Akım"), max_length=255, null=True, blank=True)
    voltaj = models.CharField(_("Voltaj"), max_length=255, null=True, blank=True)
    devir = models.CharField(_("Devir"), max_length=255, null=True, blank=True)
    ikaz_akimi = models.CharField(_("İkaz Akımı"), max_length=255, null=True, blank=True)
    ikaz_voltaji = models.CharField(_("İkaz Voltajı"), max_length=255, null=True, blank=True)
    gelis_nedeni = models.CharField(_("Geliş Nedeni"), max_length=255, null=True, blank=True)
    parca = models.BooleanField(_("Parça"), null=True, blank=True)
    eksik_malzemeler = models.CharField(_("Eksik Malzemeler"), max_length=255, null=True, blank=True)
    monte = models.BooleanField(_("Monte"), null=True, blank=True)
    demonte = models.BooleanField(_("Demonte"), null=True, blank=True)
    kasnak_kaplin = models.BooleanField(_("Kasnak/Kaplin"), null=True, blank=True)
    fan_tasi = models.BooleanField(_("Fan Taşı"), null=True, blank=True)
    ayaklar = models.BooleanField(_("Ayaklar"), null=True, blank=True)
    kama = models.BooleanField(_("Kama"), null=True, blank=True)
    klemens = models.BooleanField(_("Klemens"), null=True, blank=True)
    fircalar = models.BooleanField(_("Fırçalar"), null=True, blank=True)
    on_kapak = models.BooleanField(_("Ön Kapak"), null=True, blank=True)
    klemens_kapagi_kut = models.BooleanField(_("Klemens Kapağı/Kut"), null=True, blank=True)
    komurlar = models.BooleanField(_("Kömürler"), null=True, blank=True)
    arka_kapak = models.BooleanField(_("Arka Kapak"), null=True, blank=True)
    fan_pervane = models.BooleanField(_("Fan Pervane"), null=True, blank=True)
    rulmanlar = models.BooleanField(_("Rulmanlar"), null=True, blank=True)
    rulman_numarasi_on = models.CharField(_("Rulman Numarası Ön"), max_length=255, null=True, blank=True)
    rulman_numarasi_arka = models.CharField(_("Rulman Numarası Arka"), max_length=255, null=True, blank=True)
    demonte_eden = models.CharField(_("Demonte Eden"), max_length=255, null=True, blank=True)
    demonte_tarih = models.DateField(_("Demonte Tarih"), null=True, blank=True)
    saran_onaran = models.CharField(_("Saran/Onaran"), max_length=255, null=True, blank=True)
    saran_onaran_tarih = models.DateField(_("Saran/Onaran Tarih"), null=True, blank=True)
    monte_eden = models.CharField(_("Monte Eden"), max_length=255, null=True, blank=True)
    monte_eden_tarih = models.DateField(_("Monte Eden Tarih"), null=True, blank=True)
    test_eden = models.CharField(_("Test Eden"), max_length=255, null=True, blank=True)
    test_eden_tarih = models.DateField(_("Test Eden Tarih"), null=True, blank=True)
    izolasyon_degerleri = models.CharField(_("İzolasyon Değerleri"), max_length=25)
    calisma_akimi = models.CharField(_("Çalışma Akımı"), max_length=255, null=True, blank=True)
    calisma_gerilimi = models.CharField(_("Çalışma Gerilimi"), max_length=255, null=True, blank=True)
    diger_olcum_degerleri = models.CharField(_("Diğer Ölçüm Değerleri"), max_length=255, null=True, blank=True)
    test_cihazlari = models.CharField(_("Test Cihazları"), max_length=255, null=True, blank=True)
    yapilan_islemler = models.TextField(_("Yapılan İşlemler"), max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tersane + " - " + self.gemi
