from django.db import models
from django.contrib.auth.models import User

class Pagina(models.Model):
    # guarda os dados da revista ou do influenciador
    nome = models.CharField(max_length=100)
    tag_oficial = models.CharField(max_length=50, unique=True)
    email_contato = models.EmailField()
    telefone_emergencia = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome


class PerfilFuncionario(models.Model):
    # cada um tem seu proprio login seguro do django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # jogo o cara pra dentro de uma pagina especifica
    pagina = models.ForeignKey(Pagina, on_delete=models.CASCADE, related_name='equipe')
    
    # defino o que ele pode ou nao fazer na api
    CARGOS = [
        ('dono', 'Dono / Administrador'),
        ('editor', 'Editor de Conteúdo'),
        ('revisor', 'Revisor de Texto'),
    ]
    cargo = models.CharField(max_length=20, choices=CARGOS, default='editor')

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"


class Post(models.Model):
    STATUS_CHOICES = (
        ("rascunho", "Rascunho"),
        ("publicado", "Publicado"),
    )
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    
    # Melhoria P1: Autor agora é uma chave estrangeira real, não um texto solto
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # ligo o post a pagina (separei com null=True pra nao quebrar os dados antigos)
    pagina = models.ForeignKey(Pagina, on_delete=models.CASCADE, related_name='posts_publicados', null=True, blank=True)
    
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="rascunho"
    )
    
    # Melhoria P1: Rastreabilidade temporal para ordenação na API
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo