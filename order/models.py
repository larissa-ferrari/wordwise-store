from django.db import models
from user.models import Cliente, Endereco
from book.models import Livro


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50)
    cd_rastreamento = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Pedido {self.id}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        unique_together = ("pedido", "livro")

    def __str__(self):
        return f"{self.livro} x {self.quantidade}"
