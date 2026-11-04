from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ("rascunho", "Rascunho"),
        ("publicado", "Publicado"),
    )
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    
    # Melhoria P1: Autor agora é uma chave estrangeira real, não um texto solto
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="rascunho"
    )
    
    # Melhoria P1: Rastreabilidade temporal para ordenação na API
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo