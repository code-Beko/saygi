from django import forms
from .models import Dokuman


class DokumanForm(forms.ModelForm):
    class Meta:
        model = Dokuman
        fields = ["baslik", "dosya"]
