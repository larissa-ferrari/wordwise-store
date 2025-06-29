from django.db import models
from user.models import Cliente  

class Suporte(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    resposta = models.TextField(blank=True, null=True)
    data_resposta = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Suporte #{self.pk} - Cliente: {self.cliente}"