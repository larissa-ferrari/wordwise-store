from django.contrib import admin
from .models import Suporte
from .forms import SuporteForm
from django.utils import timezone

@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ["id", "cliente", "status", "data_envio", "data_resposta"]
    list_filter = ["status"]
    search_fields = ["mensagem", "resposta"]
    form = SuporteForm

    def save_model(self, request, obj, form, change):
        if obj.resposta and not obj.data_resposta:
            obj.data_resposta = timezone.now()
        super().save_model(request, obj, form, change)