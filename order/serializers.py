from rest_framework import serializers
from .models import Pedido, ItemPedido, Transporte, MetodoPagamento
from book.serializers import LivroSerializer


class TransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporte
        fields = "__all__"


class MetodoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPagamento
        fields = "__all__"


class ItemPedidoSerializer(serializers.ModelSerializer):
    livro = LivroSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = ["id", "livro", "quantidade", "preco_unitario", "subtotal"]

    def get_subtotal(self, obj):
        return obj.subtotal


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    transporte = TransporteSerializer(read_only=True)
    metodo_pagamento = MetodoPagamentoSerializer(read_only=True)
    total_itens = serializers.SerializerMethodField()
    total_produtos = serializers.SerializerMethodField()
    total_pedido = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            "id",
            "codigo",
            "status",
            "data_criacao",
            "transporte",
            "metodo_pagamento",
            "endereco_entrega",
            "itens",
            "total_itens",
            "total_produtos",
            "total_pedido",
            "observacoes",
        ]

    def get_total_itens(self, obj):
        return obj.total_itens

    def get_total_produtos(self, obj):
        return obj.total_produtos

    def get_total_pedido(self, obj):
        return obj.total_pedido


class CriarPedidoSerializer(serializers.ModelSerializer):
    transporte_id = serializers.PrimaryKeyRelatedField(
        queryset=Transporte.objects.filter(ativo=True), write_only=True
    )
    metodo_pagamento_id = serializers.PrimaryKeyRelatedField(
        queryset=MetodoPagamento.objects.filter(ativo=True), write_only=True
    )

    class Meta:
        model = Pedido
        fields = [
            "transporte_id",
            "metodo_pagamento_id",
            "endereco_entrega",
            "observacoes",
        ]
