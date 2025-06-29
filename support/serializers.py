from rest_framework import serializers
from .models import Suporte

class SuporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suporte
        fields = "__all__"
        read_only_fields = ["cliente", "data_envio", "data_resposta"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["cliente"] = user.cliente  # preenche com o cliente logado
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Apenas admin pode alterar resposta ou status
        user = self.context["request"].user
        if not user.is_staff:
            validated_data.pop("resposta", None)
            validated_data.pop("data_resposta", None)
            validated_data.pop("status", None)

        # Se resposta for preenchida, registra data_resposta
        if "resposta" in validated_data and validated_data["resposta"]:
            from django.utils import timezone
            validated_data["data_resposta"] = timezone.now()

        return super().update(instance, validated_data)
