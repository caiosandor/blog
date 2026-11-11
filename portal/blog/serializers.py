from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # Converte os IDs de autor e pagina para os nomes legiveis no JSON
    autor = serializers.StringRelatedField(read_only=True)
    pagina = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        # Define os campos exatos que serao serializados
        fields = [
            'id', 
            'titulo', 
            'conteudo', 
            'autor', 
            'pagina',
            'status', 
            'criado_em', 
            'atualizado_em'
        ]

    def validate(self, data):
        # Valida as regras antes de aceitar a requisicao da API
        status = data.get('status')
        conteudo = data.get('conteudo')

        if status == 'publicado' and conteudo:
            if len(conteudo.strip()) < 50:
                raise serializers.ValidationError(
                    {"conteudo": "Para ser publicado, o conteúdo da notícia deve ter no mínimo 50 caracteres."}
                )
                
        return data