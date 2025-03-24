from django import forms
from .models import Dokuman


class DokumanForm(forms.ModelForm):
    class Meta:
        model = Dokuman
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DokumanForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():

            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = ""

            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] += " form-control"

            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs["placeholder"] = f" {field.label}"

            if isinstance(field.widget, forms.DateInput):
                field.widget.attrs["placeholder"] = "YYYY-MM-DD"

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] += " form-check-input"

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
