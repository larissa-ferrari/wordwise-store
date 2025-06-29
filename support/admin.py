from django.contrib import admin
from .models import Suporte
from .forms import SuporteForm

@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ["id", "cliente", "status", "data_envio", "data_resposta"]
    list_filter = ["status"]
    search_fields = ["mensagem", "resposta"]
    form = SuporteForm
