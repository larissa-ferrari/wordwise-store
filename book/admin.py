from django.contrib import admin
from .models import Livro, Avaliacao, ClienteFavoritos


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "preco", "estoque", "status", "categoria")
    list_filter = ("status", "categoria", "tipo", "idioma")
    search_fields = ("titulo", "autor", "isbn")
    prepopulated_fields = {}
    ordering = ("titulo",)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("livro", "cliente", "nota", "data_avaliacao")
    list_filter = ("nota", "data_avaliacao")
    search_fields = ("livro__titulo", "cliente__username", "comentario")
    date_hierarchy = "data_avaliacao"


@admin.register(ClienteFavoritos)
class ClienteFavoritosAdmin(admin.ModelAdmin):
    list_display = ("cliente", "livro")
    search_fields = ("cliente__username", "livro__titulo")
