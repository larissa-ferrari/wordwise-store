from rest_framework import serializers
from .models import User, Cliente, Endereco
import re


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "birth_date",
            "password",
            "is_staff",
            "is_active",
        ]


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    enderecos = EnderecoSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = ["user", "cpf", "enderecos"]


    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        instance = super().update(instance, validated_data)

        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        return instance

class CriarClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    password = serializers.CharField(write_only=True, required=True)
    cpf = serializers.CharField(required=True)

    class Meta:
        model = Cliente
        fields = ["user", "password", "cpf"]

    def validate_cpf(self, value):
        cpf = re.sub(r"[^0-9]", "", value)

        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos")

        return cpf

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = validated_data.pop("password")
        cpf = validated_data.pop("cpf")

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            phone=user_data.get("phone", ""),
            birth_date=user_data.get("birth_date", None),
            password=password,
            user_type="cliente",
        )

        cliente = Cliente.objects.create(user=user, cpf=cpf)
        return cliente
