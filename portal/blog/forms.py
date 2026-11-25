from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'status']


class PeriodoForm(forms.Form):
    # Validação de datas recebidas via query string
    inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )


def filtrar_periodo(request, qs):
    # Aplica o filtro de intervalo de datas apenas se os parâmetros forem válidos
    form = PeriodoForm(request.GET)
    if form.is_valid():
        inicio = form.cleaned_data.get('inicio')
        fim = form.cleaned_data.get('fim')
        if inicio:
            qs = qs.filter(criado_em__date__gte=inicio)
        if fim:
            qs = qs.filter(criado_em__date__lte=fim)
    return qs, form