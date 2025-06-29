from django import forms
from .models import Suporte

class SuporteForm(forms.ModelForm):
    class Meta:
        model = Suporte
        fields = ["cliente", "mensagem", "resposta", "status"]