from django.contrib import admin
from .models import Pagina, PerfilFuncionario

# Registra a entidade central para gerenciamento no painel
@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tag_oficial')
    search_fields = ('nome', 'tag_oficial')

# Registra os perfis de acesso vinculados aos usuarios do sistema
@admin.register(PerfilFuncionario)
class PerfilFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pagina', 'cargo')
    list_filter = ('pagina', 'cargo')
    search_fields = ('usuario__username',)