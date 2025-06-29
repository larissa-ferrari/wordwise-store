from rest_framework import serializers
from .models import Carrinho, ItemCarrinho
from book.serializers import LivroSerializer


class ItemCarrinhoSerializer(serializers.ModelSerializer):
    livro = LivroSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrinho
        fields = ("id", "livro", "quantidade", "subtotal")

    def get_subtotal(self, obj):
        return obj.subtotal


class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, source="itemcarrinho_set")
    total_itens = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = (
            "id",
            "identificador",
            "cliente",
            "status",
            "itens",
            "total_itens",
            "valor_total",
        )

    def get_total_itens(self, obj):
        return obj.total_itens

    def get_valor_total(self, obj):
        return obj.valor_total


class AdicionarItemSerializer(serializers.Serializer):
    livro_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(default=1, min_value=1)
