from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone", "birth_date", "is_staff", "is_active"]
