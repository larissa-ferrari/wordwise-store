from django.db import models
from django.core.validators import MinValueValidator
from user.models import Cliente
from book.models import Livro
import uuid


class Transporte(models.Model):
    TIPOS_TRANSPORTE = [
        ("PAC", "Envio Econômico (PAC)"),
        ("SEDEX", "SEDEX"),
        ("RETIRADA", "Retirar na Loja"),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_TRANSPORTE)
    prazo_dias = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()}) - R${self.valor}"


class MetodoPagamento(models.Model):
    TIPOS_PAGAMENTO = [
        ("CARTAO", "Cartão de Crédito"),
        ("BOLETO", "Boleto Bancário"),
        ("PIX", "PIX"),
        ("DINHEIRO", "Dinheiro na Entrega"),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_PAGAMENTO)
    ativo = models.BooleanField(default=True)
    taxas = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Pedido(models.Model):
    STATUS_PEDIDO = [
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("ENVIADO", "Enviado"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADO", "Cancelado"),
    ]

    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, blank=True
    )
    session_key = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_PEDIDO, default="PENDENTE")
    transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT)
    metodo_pagamento = models.ForeignKey(MetodoPagamento, on_delete=models.PROTECT)
    endereco_entrega = models.JSONField()
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_status_display()}"

    @property
    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())

    @property
    def total_produtos(self):
        return sum(item.subtotal for item in self.itens.all())

    @property
    def total_pedido(self):
        return self.total_produtos + self.transporte.valor


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="itens", on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("pedido", "livro")

    def __str__(self):
        return f"{self.livro.titulo} x {self.quantidade}"

    @property
    def subtotal(self):
        if self.preco_unitario is None or self.quantidade is None:
            return 0
        return self.preco_unitario * self.quantidade
