from django.db import models
from django.contrib.auth.models import User
from core.models import DaOrganizacao

# Herda os campos de DaOrganizacao, recebendo a chave estrangeira da página automaticamente
class Post(DaOrganizacao):
    STATUS_CHOICES = (
        ("rascunho", "Rascunho"),
        ("publicado", "Publicado"),
    )
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    
    # Mantém o autor ligado ao usuário padrão do Django
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # OBS: O campo 'pagina' não precisa mais ser digitado aqui, 
    # pois ele é herdado automaticamente da classe DaOrganizacao.
    
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="rascunho"
    )
    
    # Rastreabilidade temporal para ordenação
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo