from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # Regra da aula: Listar os campos explicitamente. Evitar o uso de "__all__".
        fields = [
            'id', 
            'titulo', 
            'conteudo', 
            'autor', 
            'status', 
            'criado_em', 
            'atualizado_em'
        ]

    def validate(self, data):
        """
        Validação de regras de negócio (Substitui o clean() do forms.py).
        Garante que a API não aceite posts inválidos vindos do Postman/Frontend.
        """
        status = data.get('status')
        conteudo = data.get('conteudo')

        # Regra da P1: Validar tamanho mínimo se o status for "publicado"
        if status == 'publicado' and conteudo:
            if len(conteudo.strip()) < 50:
                raise serializers.ValidationError(
                    {"conteudo": "Para ser publicado, o conteúdo da notícia deve ter no mínimo 50 caracteres."}
                )
                
        return data