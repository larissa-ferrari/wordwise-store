from django.contrib import admin
from .models import Pedido, ItemPedido, Transporte, MetodoPagamento


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ["subtotal"]
    fields = ["livro", "quantidade", "preco_unitario", "subtotal"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "cliente", "status", "total_pedido", "data_criacao"]
    list_filter = ["status", "data_criacao"]
    search_fields = ["codigo", "cliente__user__username"]
    inlines = [ItemPedidoInline]
    readonly_fields = ["total_pedido", "data_criacao", "data_atualizacao"]


@admin.register(Transporte)
class TransporteAdmin(admin.ModelAdmin):
    list_display = ["nome", "tipo", "valor", "prazo_dias", "ativo"]
    list_editable = ["ativo"]
    list_filter = ["tipo", "ativo"]


@admin.register(MetodoPagamento)
class MetodoPagamentoAdmin(admin.ModelAdmin):
    list_display = ["nome", "tipo", "taxas", "ativo"]
    list_editable = ["ativo"]
    list_filter = ["tipo", "ativo"]
