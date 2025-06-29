from django import forms
from .models import Cliente, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "user_type",
            "is_staff",
            "is_active",
        ]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["user", "cpf"]
