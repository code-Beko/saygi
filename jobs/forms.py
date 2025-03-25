from django import forms
from .models import Dokuman


class DokumanForm(forms.ModelForm):
    class Meta:
        model = Dokuman
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DokumanForm, self).__init__(*args, **kwargs)

        # Tüm alanlara form-control class'ını ekliyoruz (boolean dışındaki alanlar)
        for field in self.fields.values():
            # Eğer widget'ta 'class' özelliği yoksa, onu oluşturuyoruz
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = ""

            # Boolean alanları hariç tutuyoruz
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] += " form-control mb-3 "

            # Placeholder ekliyoruz
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs["placeholder"] = f" {field.label}"

            # Date alanları için placeholder
            if isinstance(field.widget, forms.DateInput):
                field.widget.attrs["placeholder"] = "YYYY-MM-DD"

            # Boolean alanları için CheckboxInput widget'ı
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] += " form-check-input mb-4"

            # Tüm alanlar isteğe bağlı (boş bırakılabilir) olacak şekilde ayarlıyoruz
            field.required = False  # Bütün alanları isteğe bağlı yapıyoruz

        # Tarih alanları için date tipi ve form-control ekleme
        date_fields = [
            "tarih",
            "demonte_tarih",
            "saran_onaran_tarih",
            "monte_eden_tarih",
            "test_eden_tarih",
        ]
        for field_name in date_fields:
            self.fields[field_name].widget = forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            )
