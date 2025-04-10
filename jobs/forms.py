from django import forms
from .models import Document, Task, Department
from .fields import get_document_fields
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


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
            "shipyard": forms.TextInput(attrs={"class": "form-control"}),
            "boat": forms.TextInput(attrs={"class": "form-control"}),
            "engine_name": forms.TextInput(attrs={"class": "form-control"}),
            "job_number": forms.TextInput(attrs={"class": "form-control"}),
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "device_receiver": forms.TextInput(attrs={"class": "form-control"}),
            "device_type": forms.TextInput(attrs={"class": "form-control"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "device_brand": forms.TextInput(attrs={"class": "form-control"}),
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "power": forms.TextInput(attrs={"class": "form-control"}),
            "current": forms.TextInput(attrs={"class": "form-control"}),
            "voltage": forms.TextInput(attrs={"class": "form-control"}),
            "rpm": forms.TextInput(attrs={"class": "form-control"}),
            "warning_current": forms.TextInput(attrs={"class": "form-control"}),
            "warning_voltage": forms.TextInput(attrs={"class": "form-control"}),
            "arrival_reason": forms.TextInput(attrs={"class": "form-control"}),
            "missing_materials": forms.TextInput(attrs={"class": "form-control"}),
            "front_bearing_number": forms.TextInput(attrs={"class": "form-control"}),
            "back_bearing_number": forms.TextInput(attrs={"class": "form-control"}),
            "dismounted_by": forms.TextInput(attrs={"class": "form-control"}),
            "wrapped_repaired_by": forms.TextInput(attrs={"class": "form-control"}),
            "mounted_by": forms.TextInput(attrs={"class": "form-control"}),
            "tested_by": forms.TextInput(attrs={"class": "form-control"}),
            "insulation_values": forms.TextInput(attrs={"class": "form-control"}),
            "operating_current": forms.TextInput(attrs={"class": "form-control"}),
            "operating_voltage": forms.TextInput(attrs={"class": "form-control"}),
            "other_measurement_values": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "test_devices": forms.TextInput(attrs={"class": "form-control"}),
            "performed_operations": forms.TextInput(attrs={"class": "form-control"}),
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
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Departman Seçiniz",
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
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = False
        user.is_staff = True
        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user and not self.user.is_superuser:
            # Kullanıcının departmanını al
            department = self.user.department
            if department:
                # Sadece kullanıcının departmanındaki kullanıcıları göster
                self.fields["assigned_to"].queryset = CustomUser.objects.filter(
                    department=department
                )
                # Departman alanını devre dışı bırak
                self.fields["department"].disabled = True

    class Meta:
        model = Task
        fields = [
            "company_name",
            "ship_name",
            "company_representative",
            "project_name",
            "description",
            "date",
            "finished_date",
            "status",
            "department",
            "assigned_to",
            "transactions_made",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "ship_name": forms.TextInput(attrs={"class": "form-control"}),
            "company_representative": forms.TextInput(attrs={"class": "form-control"}),
            "project_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "finished_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "transactions_made": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
            "assigned_to": forms.SelectMultiple(attrs={"class": "form-control"}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
        }
