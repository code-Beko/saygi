from django import forms
from .models import Dokuman
from .fields import get_dokuman_fields
from django.utils.translation import gettext as _


class DokumanForm(forms.ModelForm):
    class Meta:
        model = Dokuman
        fields = "__all__"
        widgets = {
            'tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'demonte_tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'saran_onaran_tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'monte_eden_tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'test_eden_tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(DokumanForm, self).__init__(*args, **kwargs)

        fields_info = get_dokuman_fields(self.instance)
        
        # Form alanlarını fields_info sırasına göre yeniden düzenle
        self.fields = {field_info["name"]: self.fields[field_info["name"]] for field_info in fields_info if field_info["name"] in self.fields}

        for field_info in fields_info:
            field_name = field_info["name"]

            if field_name in self.fields:
                field_size = field_info["size"]
                field_type = field_info["type"]

                self.fields[field_name].widget.attrs["size"] = field_size
                self.fields[field_name].required = False  # Tüm alanları opsiyonel yap

                if field_type == "checkbox":
                    self.fields[field_name].widget = forms.CheckboxInput(
                        attrs={
                            "class": "form-check-input",
                            "type": "checkbox",
                            "size": field_size,
                        }
                    )
                elif field_type == "date":
                    self.fields[field_name].widget = forms.DateInput(
                        attrs={
                            "type": "date",
                            "class": "form-control",
                            "size": field_size,
                        },
                        format='%Y-%m-%d'
                    )
                    if self.instance and getattr(self.instance, field_name):
                        self.fields[field_name].initial = getattr(self.instance, field_name).strftime('%Y-%m-%d')
                else:
                    self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields_order = [
            field_info["name"]
            for field_info in fields_info
            if field_info["name"] in self.fields
        ]
