from django import forms
from .models import Dokuman


class DokumanForm(forms.ModelForm):
    class Meta:
        model = Dokuman
        fields = ["baslik", "dosya"]

    def __init__(self, *args, **kwargs):
        super(DokumanForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                field.widget.attrs.get("class", "") + " form-control"
            )
