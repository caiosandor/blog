import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import Post
from .forms import PostForm, filtrar_periodo
from .serializers import PostSerializer
from .dashboard import obter_metricas_dashboard


@login_required
def lista_posts(request):
    # Uso de select_related para evitar consultas N+1 ao acessar dados do autor
    posts = Post.objects.filter(
        pagina=request.user.perfilfuncionario.pagina
    ).select_related('autor')
    
    busca_texto = request.GET.get('q')
    busca_status = request.GET.get('status')
    
    filtros = Q()
    if busca_texto:
        filtros &= Q(titulo__icontains=busca_texto)
    if busca_status:
        filtros &= Q(status=busca_status)
        
    if filtros:
        posts = posts.filter(filtros)
    else:
        posts = posts.filter(status='publicado')

    return render(request, 'blog/lista.html', {'posts': posts})


@login_required
def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.pagina = request.user.perfilfuncionario.pagina
            post.save()
            return redirect('lista')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {'form': form})


@login_required
def post_detalhe(request, id):
    post = get_object_or_404(
        Post.objects.select_related('autor'),
        id=id,
        pagina=request.user.perfilfuncionario.pagina
    )
    return render(request, 'blog/detalhe.html', {'post': post})


@login_required
def lista_rascunhos(request):
    rascunhos = Post.objects.filter(
        pagina=request.user.perfilfuncionario.pagina,
        status='rascunho'
    ).select_related('autor')
    return render(request, 'blog/rascunhos.html', {'posts': rascunhos})


@login_required
def editar_post(request, id):
    post = get_object_or_404(Post, id=id, pagina=request.user.perfilfuncionario.pagina)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalhe', id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/form.html', {'form': form, 'post': post})


@login_required
def excluir_post(request, id):
    post = get_object_or_404(Post, id=id, pagina=request.user.perfilfuncionario.pagina)
    if request.method == 'POST':
        post.delete()
        return redirect('lista')
    return render(request, 'blog/excluir.html', {'post': post})


@login_required
def dashboard_view(request):
    perfil = request.user.perfilfuncionario
    minha_pagina = perfil.pagina

    base_qs = Post.objects.filter(pagina=minha_pagina)
    qs_filtrada, form = filtrar_periodo(request, base_qs)

    metricas = obter_metricas_dashboard(minha_pagina, qs_posts=qs_filtrada)

    contexto = {
        **metricas,
        'pagina': minha_pagina,
        'form': form,
        'mostra_series': perfil.eh_admin,
        'pode_exportar': perfil.eh_admin,
    }
    return render(request, 'blog/dashboard.html', contexto)


@login_required
def exportar_posts_csv(request):
    perfil = request.user.perfilfuncionario
    if not perfil.eh_admin:
        return HttpResponseForbidden('Acesso restrito a administradores da página.')

    minha_pagina = perfil.pagina
    base_qs = (
        Post.objects.filter(pagina=minha_pagina)
        .select_related('autor')
        .order_by('-criado_em')
    )
    qs_filtrada, _ = filtrar_periodo(request, base_qs)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="relatorio_posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Título', 'Autor', 'Status', 'Criado em', 'Atualizado em'])

    for post in qs_filtrada:
        # Sanitização para prevenir injeção de fórmulas em planilhas (CSV Injection)
        titulo = post.titulo
        if titulo and titulo[0] in ('=', '+', '-', '@'):
            titulo = f"'{titulo}"

        writer.writerow([
            titulo,
            post.autor.get_full_name() or post.autor.username,
            post.get_status_display(),
            post.criado_em.strftime('%d/%m/%Y %H:%M'),
            post.atualizado_em.strftime('%d/%m/%Y %H:%M'),
        ])

    return response


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfilfuncionario'):
            return Post.objects.filter(
                pagina=user.perfilfuncionario.pagina
            ).select_related('autor')
        return Post.objects.none() 

    def perform_create(self, serializer):
        serializer.save(
            autor=self.request.user, 
            pagina=self.request.user.perfilfuncionario.pagina
        )