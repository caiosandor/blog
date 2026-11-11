from django.db import models
from django.contrib.auth.models import User

# Entidade central para o isolamento de dados (Multi-tenant)
class Pagina(models.Model):
    nome = models.CharField(max_length=120)
    tag_oficial = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome

# Base abstrata para compartilhar a ForeignKey com os models de negócio sem duplicar código
class DaOrganizacao(models.Model):
    # Aceita nulo temporariamente para não quebrar o banco na migração dos dados legados
    pagina = models.ForeignKey(Pagina, on_delete=models.PROTECT, null=True)

    class Meta:
        abstract = True

# Gerencia o vínculo do usuário com a página e seu nível de acesso na aplicação
class PerfilFuncionario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pagina = models.ForeignKey(Pagina, on_delete=models.PROTECT)
    
    CARGOS = [('dono', 'Dono'), ('editor', 'Editor')]
    cargo = models.CharField(max_length=20, choices=CARGOS, default='editor')

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"