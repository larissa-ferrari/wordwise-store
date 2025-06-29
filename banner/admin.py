from django.contrib import admin
from .models import Banner
from .forms import BannerForm

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["id", "titulo", "visivel", "prioridade", "posicao", "dt_criacao"]
    list_filter = ["visivel", "posicao"]
    search_fields = ["titulo", "link_destino"]
    ordering = ["-prioridade", "-dt_criacao"]
    form = BannerForm
