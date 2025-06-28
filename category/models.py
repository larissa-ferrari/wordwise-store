from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    imagem_url = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return self.nome
