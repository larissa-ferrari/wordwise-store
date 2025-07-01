from rest_framework import serializers
from .models import Livro, Avaliacao, ClienteFavoritos


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = "__all__"
        read_only_fields = ("status",)


class AvaliacaoSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    livro = serializers.StringRelatedField()
    livro_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Avaliacao
        fields = "__all__"
        read_only_fields = ("data_avaliacao",)


class ClienteFavoritosSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    livro = serializers.StringRelatedField()

    class Meta:
        model = ClienteFavoritos
        fields = "__all__"
