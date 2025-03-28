from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _


# CustomUser model
class CustomUser(AbstractUser):
    DEPARTMAN_CHOICES = [
        ('otomasyon', 'Otomasyon'),
        ('yeni_insa', 'Yeni İnşa'),
        ('bakim', 'Bakım'),
        ('kalite', 'Kalite'),
        ('diger', 'Diğer'),
    ]

    YETKI_CHOICES = [
        ('yetki1', 'Tam Yetki'),
        ('yetki2', 'Yüksek Yetki'),
        ('yetki3', 'Orta Yetki'),
        ('yetki4', 'Düşük Yetki'),
        ('yetki5', 'Sınırlı Yetki'),
    ]

    phone_number = models.CharField(
        _("Telefon Numarası"), max_length=15, blank=True, null=True
    )
    department = models.CharField(
        _("Departman"), max_length=20, choices=DEPARTMAN_CHOICES, default='diger'
    )
    yetki = models.CharField(
        _("Yetki Seviyesi"), max_length=10, choices=YETKI_CHOICES, default='yetki5'
    )

    def has_full_access(self):
        return self.yetki == 'yetki1'

    def has_high_access(self):
        return self.yetki in ['yetki1', 'yetki2']

    def has_medium_access(self):
        return self.yetki in ['yetki1', 'yetki2', 'yetki3']

    def has_low_access(self):
        return self.yetki in ['yetki1', 'yetki2', 'yetki3', 'yetki4']

    def is_automation_department(self):
        return self.department == 'otomasyon'

    def is_new_construction_department(self):
        return self.department == 'yeni_insa'

    def is_maintenance_department(self):
        return self.department == 'bakim'

    def is_quality_department(self):
        return self.department == 'kalite'


# Document model
class Document(models.Model):
    shipyard = models.CharField(_("Shipyard"), max_length=255, null=True, blank=True)
    boat = models.CharField(_("Boat"), max_length=255, null=True, blank=True)
    engine_name = models.CharField(
        _("Engine Name"), max_length=255, null=True, blank=True
    )
    job_number = models.CharField(
        _("Job Number"), max_length=255, null=True, blank=True
    )
    customer_name = models.CharField(
        _("Customer Name"), max_length=255, null=True, blank=True
    )
    date = models.DateField(_("Date"), null=True, blank=True, default=date.today)
    device_receiver = models.CharField(
        _("Device Receiver"), max_length=255, null=True, blank=True
    )
    device_type = models.CharField(
        _("Device Type"), max_length=255, null=True, blank=True
    )
    model = models.CharField(_("Model"), max_length=255, null=True, blank=True)
    device_brand = models.CharField(
        _("Device Brand"), max_length=255, null=True, blank=True
    )
    serial_number = models.CharField(
        _("Serial Number"), max_length=255, null=True, blank=True
    )
    power = models.CharField(_("Power"), max_length=255, null=True, blank=True)
    current = models.CharField(_("Current"), max_length=255, null=True, blank=True)
    voltage = models.CharField(_("Voltage"), max_length=255, null=True, blank=True)
    rpm = models.CharField(_("RPM"), max_length=255, null=True, blank=True)
    warning_current = models.CharField(
        _("Warning Current"), max_length=255, null=True, blank=True
    )
    warning_voltage = models.CharField(
        _("Warning Voltage"), max_length=255, null=True, blank=True
    )
    arrival_reason = models.CharField(
        _("Arrival Reason"), max_length=255, null=True, blank=True
    )
    part = models.BooleanField(_("Part"), null=True, blank=True)
    missing_materials = models.CharField(
        _("Missing Materials"), max_length=255, null=True, blank=True
    )
    mount = models.BooleanField(_("Mount"), null=True, blank=True)
    dismount = models.BooleanField(_("Dismount"), null=True, blank=True)
    pulley_coupling = models.BooleanField(_("Pulley/Coupling"), null=True, blank=True)
    fan_carrier = models.BooleanField(_("Fan Carrier"), null=True, blank=True)
    feet = models.BooleanField(_("Feet"), null=True, blank=True)
    key = models.BooleanField(_("Key"), null=True, blank=True)
    terminal = models.BooleanField(_("Terminal"), null=True, blank=True)
    brushes = models.BooleanField(_("Brushes"), null=True, blank=True)
    front_cover = models.BooleanField(_("Front Cover"), null=True, blank=True)
    terminal_cover_box = models.BooleanField(
        _("Terminal Cover/Box"), null=True, blank=True
    )
    carbon_brushes = models.BooleanField(_("Carbon Brushes"), null=True, blank=True)
    back_cover = models.BooleanField(_("Back Cover"), null=True, blank=True)
    fan_blade = models.BooleanField(_("Fan Blade"), null=True, blank=True)
    bearings = models.BooleanField(_("Bearings"), null=True, blank=True)
    front_bearing_number = models.CharField(
        _("Front Bearing Number"), max_length=255, null=True, blank=True
    )
    back_bearing_number = models.CharField(
        _("Back Bearing Number"), max_length=255, null=True, blank=True
    )
    dismounted_by = models.CharField(
        _("Dismounted By"), max_length=255, null=True, blank=True
    )
    dismount_date = models.DateField(_("Dismount Date"), null=True, blank=True)
    wrapped_repaired_by = models.CharField(
        _("Wrapped/Repaired By"), max_length=255, null=True, blank=True
    )
    wrap_repair_date = models.DateField(_("Wrap/Repair Date"), null=True, blank=True)
    mounted_by = models.CharField(
        _("Mounted By"), max_length=255, null=True, blank=True
    )
    mount_date = models.DateField(_("Mount Date"), null=True, blank=True)
    tested_by = models.CharField(_("Tested By"), max_length=255, null=True, blank=True)
    test_date = models.DateField(_("Test Date"), null=True, blank=True)
    insulation_values = models.CharField(_("Insulation Values"), max_length=25)
    operating_current = models.CharField(
        _("Operating Current"), max_length=255, null=True, blank=True
    )
    operating_voltage = models.CharField(
        _("Operating Voltage"), max_length=255, null=True, blank=True
    )
    other_measurement_values = models.CharField(
        _("Other Measurement Values"), max_length=255, null=True, blank=True
    )
    test_devices = models.CharField(
        _("Test Devices"), max_length=255, null=True, blank=True
    )
    performed_operations = models.TextField(_("Performed Operations"), max_length=255)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_documents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shipyard + " - " + self.boat


class Task(models.Model):
    STATUS_CHOICES = [
        ('beklemede', 'Beklemede'),
        ('devam_ediyor', 'Devam Ediyor'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal'),
        ('ertelendi', 'Ertelendi'),
    ]

    project_name = models.CharField(_("Proje Adı"), max_length=255)
    description = models.TextField(_("Açıklama"))
    date = models.DateField(_("Tarih"), default=date.today)
    status = models.CharField(_("Durum"), max_length=20, choices=STATUS_CHOICES, default='beklemede')
    department = models.CharField(_("Departman"), max_length=20, choices=CustomUser.DEPARTMAN_CHOICES)
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks')
    is_read = models.ManyToManyField(CustomUser, related_name='read_tasks', blank=True)

    def __str__(self):
        return self.project_name
