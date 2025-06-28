from django.db import models


class Banner(models.Model):
    titulo = models.CharField(max_length=255)
    imagem_url = models.CharField(max_length=512)
    link_destino = models.CharField(max_length=512)
    visivel = models.BooleanField(default=True)
    prioridade = models.IntegerField()
    posicao = models.CharField(max_length=100)
    dt_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
