from django.db import models
from django.contrib.auth.models import User
from core.models import DaOrganizacao


class Post(DaOrganizacao):
    STATUS_CHOICES = (
        ("rascunho", "Rascunho"),
        ("publicado", "Publicado"),
    )
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="rascunho"
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        # Índices compostos para otimizar filtros por organização, data e status
        indexes = [
            models.Index(fields=['pagina', 'criado_em']),
            models.Index(fields=['pagina', 'status']),
        ]

    def __str__(self):
        return self.titulo