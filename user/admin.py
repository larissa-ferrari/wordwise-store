from django.contrib import admin
from .models import User
from .forms import UserForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "phone", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["username", "email", "phone"]
    form = UserForm
