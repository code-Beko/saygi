from django import forms
from .models import Document
from .fields import get_document_fields
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "dismount_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "wrap_repair_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "mount_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "test_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)

        fields_info = get_document_fields(self.instance)

        self.fields = {
            field_info["name"]: self.fields[field_info["name"]]
            for field_info in fields_info
            if field_info["name"] in self.fields
        }

        for field_info in fields_info:
            field_name = field_info["name"]

            if field_name in self.fields:
                field_size = field_info["size"]
                field_type = field_info["type"]

                self.fields[field_name].widget.attrs["size"] = field_size
                self.fields[field_name].required = False

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
                        format="%Y-%m-%d",
                    )
                    if self.instance and getattr(self.instance, field_name):
                        self.fields[field_name].initial = getattr(
                            self.instance, field_name
                        ).strftime("%Y-%m-%d")
                else:
                    self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields_order = [
            field_info["name"]
            for field_info in fields_info
            if field_info["name"] in self.fields
        ]


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    department = forms.ChoiceField(
        choices=CustomUser.DEPARTMAN_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    yetki = forms.ChoiceField(
        choices=CustomUser.YETKI_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "phone_number",
            "department",
            "yetki",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = False  # Yeni kullanıcılar superuser olamaz
        user.is_staff = True  # Admin paneline erişim için staff olmalı
        if commit:
            user.save()
        return user
