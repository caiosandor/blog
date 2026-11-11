from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Define os campos do formulario expostos para o usuario
        fields = ["titulo", "conteudo", "status"]

    def clean(self):
        # Valida e recupera os dados limpos enviados no formulario
        cleaned_data = super().clean()
        conteudo = cleaned_data.get("conteudo")
        status = cleaned_data.get("status")

        # Impede a publicacao de posts com conteudo menor que 50 caracteres
        if status == 'publicado' and conteudo:
            if len(conteudo.strip()) < 50:
                raise ValidationError("Para ser publicado, o conteúdo da notícia deve ter no mínimo 50 caracteres.")
                
        return cleaned_data