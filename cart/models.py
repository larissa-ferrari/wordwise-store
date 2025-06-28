from django.db import models
from user.models import Cliente
from book.models import Livro


class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Carrinho {self.id} - {self.cliente}"


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        unique_together = ("carrinho", "livro")

    def __str__(self):
        return f"{self.livro} x {self.quantidade}"
