from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # mostra o nome do autor legivel no json em vez do id
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        # listo os campos direto sem usar __all__
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
        # trava a api e devolve erro 400 em json se a regra quebrar
        status = data.get('status')
        conteudo = data.get('conteudo')

        if status == 'publicado' and conteudo:
            if len(conteudo.strip()) < 50:
                raise serializers.ValidationError(
                    {"conteudo": "Para ser publicado, o conteúdo da notícia deve ter no mínimo 50 caracteres."}
                )
                
        return data