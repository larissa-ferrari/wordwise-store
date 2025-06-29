from django.contrib import admin
from .models import User, Cliente, Administrador, Endereco
from .forms import UserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "phone",
        "user_type",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_staff", "is_active", "user_type"]
    search_fields = ["username", "email", "phone"]
    form = UserForm


class EnderecoInline(admin.TabularInline):
    model = Endereco
    extra = 0
    fields = [
        "rua",
        "numero",
        "complemento",
        "bairro",
        "cidade",
        "estado",
        "cep",
        "pais",
        "principal",
    ]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["user_info", "total_enderecos"]
    search_fields = ["user__username", "user__email"]
    inlines = [EnderecoInline]

    def user_info(self, obj):
        return f"{obj.user.username} ({obj.user.email})"

    user_info.short_description = "Usuário"

    def total_enderecos(self, obj):
        return obj.endereco_set.count()

    total_enderecos.short_description = "Endereços"


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ["user_info", "access_level", "status"]
    list_filter = ["access_level", "status"]
    search_fields = ["user__username", "user__email"]

    def user_info(self, obj):
        return f"{obj.user.username} ({obj.user.email})"

    user_info.short_description = "Usuário"
