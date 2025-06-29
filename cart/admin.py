from django.contrib import admin
from .models import Carrinho, ItemCarrinho


class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0
    readonly_fields = ("subtotal",)
    fields = ("livro", "quantidade", "subtotal")


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "session_key",
        "status",
        "total_itens",
        "valor_total",
        "dt_criacao",
    )
    list_filter = ("status", "dt_criacao")
    search_fields = ("cliente__user__username", "session_key")
    inlines = [ItemCarrinhoInline]
    readonly_fields = ("identificador", "total_itens", "valor_total")


@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ("id", "carrinho", "livro", "quantidade", "subtotal")
    list_select_related = ("carrinho", "livro")
