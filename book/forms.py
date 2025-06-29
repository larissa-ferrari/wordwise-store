from django import forms
from .models import Livro, Avaliacao, ClienteFavoritos


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = "__all__"
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "ano_publicacao": forms.NumberInput(attrs={"min": 1000, "max": 2100}),
            "preco": forms.NumberInput(attrs={"min": 0, "step": 0.01}),
            "estoque": forms.NumberInput(attrs={"min": 0}),
            "numero_paginas": forms.NumberInput(attrs={"min": 1}),
        }


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ["nota", "comentario"]
        widgets = {
            "nota": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comentario": forms.Textarea(attrs={"rows": 4}),
        }


class ClienteFavoritosForm(forms.ModelForm):
    class Meta:
        model = ClienteFavoritos
        fields = ["livro"]
