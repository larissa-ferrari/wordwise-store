from django.db import models
from user.models import Cliente
from book.models import Livro
import uuid


class Carrinho(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="ativo")
    identificador = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        unique_together = [["cliente", "status"], ["session_key", "status"]]

    def __str__(self):
        if self.cliente:
            return f"Carrinho {self.id} - {self.cliente}"
        return f"Carrinho Sessão {self.session_key}"

    @property
    def total_itens(self):
        return sum(item.quantidade for item in self.itemcarrinho_set.all())

    @property
    def valor_total(self):
        return sum(
            item.livro.preco * item.quantidade for item in self.itemcarrinho_set.all()
        )


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    class Meta:
        unique_together = ("carrinho", "livro")

    def __str__(self):
        return f"{self.livro} x {self.quantidade}"

    @property
    def subtotal(self):
        return self.livro.preco * self.quantidade
