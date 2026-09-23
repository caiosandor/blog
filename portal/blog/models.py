from django.db import models


class Post(models.Model):
  STATUS_CHOICES = (
      ("rascunho", "Rascunho"),
      ("publicado", "Publicado"),
  )
  titulo = models.CharField(max_length=200)
  conteudo = models.TextField()
  autor = models.CharField(max_length=100)
  status = models.CharField(
      max_length=10, choices=STATUS_CHOICES, default="rascunho"
  )

  def __str__(self):
    return self.titulo