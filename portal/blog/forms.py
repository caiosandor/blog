from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "conteudo", "autor", "status"]

    def clean(self):
        cleaned_data = super().clean()
        conteudo = cleaned_data.get("conteudo")
        status = cleaned_data.get("status")

        # Regra da P1: Validar tamanho mínimo se o status for "publicado"
        if status == 'publicado' and conteudo:
            if len(conteudo.strip()) < 50:
                raise ValidationError("Para ser publicado, o conteúdo da notícia deve ter no mínimo 50 caracteres.")
                
        return cleaned_data