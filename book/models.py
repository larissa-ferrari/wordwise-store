from django.db import models
from category.models import Categoria
from user.models import Cliente


class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editora = models.CharField(max_length=255)
    ano_publicacao = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    descricao = models.TextField(blank=True)
    imagem_url = models.CharField(max_length=512, blank=True)
    isbn = models.CharField(max_length=20)
    tipo = models.CharField(max_length=100)
    numero_paginas = models.IntegerField()
    idioma = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.livro.titulo} - {self.nota} estrelas"


class ClienteFavoritos(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("cliente", "livro")

    def __str__(self):
        return f"{self.cliente} ♥ {self.livro}"
