from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = [
            "titulo", "imagem_url", "link_destino",
            "visivel", "prioridade", "posicao"
        ]
