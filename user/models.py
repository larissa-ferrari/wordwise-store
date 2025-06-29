from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user_type = models.CharField(
        max_length=20,
        choices=[("cliente", "Cliente"), ("administrador", "Administrador")],
        default="cliente",
    )

    def __str__(self):
        return self.username


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)

    def clean(self):
        if Cliente.objects.exclude(pk=self.pk).filter(cpf=self.cpf).exists():
            raise ValidationError("CPF já está em uso.")

    def __str__(self):
        return self.user.username


class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    access_level = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=20)
    pais = models.CharField(max_length=50)
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rua}, {self.numero}"
