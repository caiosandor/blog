from django.db import models
from django.contrib.auth.models import User


class Pagina(models.Model):
    nome = models.CharField(max_length=120)
    tag_oficial = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome


class DaOrganizacao(models.Model):
    # Chave estrangeira base para isolamento multi-tenant
    pagina = models.ForeignKey(Pagina, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class PerfilFuncionario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pagina = models.ForeignKey(Pagina, on_delete=models.PROTECT)
    
    CARGOS = [('dono', 'Dono'), ('editor', 'Editor')]
    cargo = models.CharField(max_length=20, choices=CARGOS, default='editor')

    @property
    def eh_admin(self):
        # Define privilégio administrativo para acesso a métricas e exportações
        return self.cargo == 'dono'

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"