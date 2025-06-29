from django.contrib import admin
from .models import Categoria
from .forms import CategoriaForm


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["id", "nome", "status"]
    list_filter = ["status"]
    search_fields = ["nome", "descricao"]
    form = CategoriaForm
