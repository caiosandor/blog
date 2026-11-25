from datetime import datetime, time
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import Pagina, PerfilFuncionario
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'status']
        labels = {
            'titulo': 'Título da Matéria',
            'conteudo': 'Conteúdo',
            'status': 'Status de Publicação',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Digite um título chamativo...'}),
            'conteudo': forms.Textarea(attrs={'placeholder': 'Escreva o corpo da matéria aqui...'}),
        }


class PeriodoForm(forms.Form):
    inicio = forms.DateField(
        required=False,
        label='Início',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    fim = forms.DateField(
        required=False,
        label='Fim',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )


def filtrar_periodo(request, queryset):
    form = PeriodoForm(request.GET or None)
    if form.is_valid():
        inicio = form.cleaned_data.get('inicio')
        fim = form.cleaned_data.get('fim')
        tz = timezone.get_current_timezone()

        if inicio:
            dt_inicio = timezone.make_aware(datetime.combine(inicio, time.min), tz)
            queryset = queryset.filter(criado_em__gte=dt_inicio)

        if fim:
            dt_fim = timezone.make_aware(datetime.combine(fim, time.max), tz)
            queryset = queryset.filter(criado_em__lte=dt_fim)

    return queryset, form


class CadastroRevistaForm(forms.Form):
    nome_revista = forms.CharField(
        label='Nome da Revista / Portal',
        max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Portal Esportes'}),
    )
    primeiro_nome = forms.CharField(
        label='Seu Nome',
        max_length=80,
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Caio Sandor'}),
    )
    username = forms.CharField(
        label='Usuário de Acesso',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: caio_esportes'}),
    )
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username


class NovoMembroEquipeForm(forms.Form):
    primeiro_nome = forms.CharField(
        label='Nome do Colaborador',
        max_length=80,
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Ana Silva'}),
    )
    username = forms.CharField(
        label='Usuário de Acesso',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: ana_editora'}),
    )
    senha = forms.CharField(
        label='Senha Provisória',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )
    cargo = forms.ChoiceField(
        label='Cargo na Redação',
        choices=[('editor', 'Editor'), ('dono', 'Dono')],
        initial='editor',
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username