import csv
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .dashboard import obter_metricas_dashboard
from .forms import PostForm, filtrar_periodo
from .models import Post


def _obter_perfil(user):
    if not user.is_authenticated:
        return None
    return getattr(user, 'perfilfuncionario', None)


def lista_posts(request):
    perfil = _obter_perfil(request.user)
    if perfil:
        posts = Post.objects.filter(pagina=perfil.pagina).select_related('autor')
    else:
        posts = Post.objects.filter(status='publicado').select_related('autor')

    busca = request.GET.get('q', '').strip()
    if busca:
        posts = posts.filter(Q(titulo__icontains=busca) | Q(conteudo__icontains=busca))

    status_filtro = request.GET.get('status', '').strip()
    if status_filtro in ('publicado', 'rascunho'):
        posts = posts.filter(status=status_filtro)

    posts = posts.order_by('-criado_em')
    return render(request, 'blog/lista.html', {'posts': posts})


@login_required
def lista_rascunhos(request):
    perfil = _obter_perfil(request.user)
    if perfil is None:
        return HttpResponseForbidden('Usuário sem perfil de funcionário associado a uma página.')

    posts = (
        Post.objects.filter(pagina=perfil.pagina, status='rascunho')
        .select_related('autor')
        .order_by('-criado_em')
    )
    return render(request, 'blog/rascunhos.html', {'posts': posts})


def post_detalhe(request, id):
    perfil = _obter_perfil(request.user)
    if perfil:
        post = get_object_or_404(Post.objects.select_related('autor'), id=id, pagina=perfil.pagina)
    else:
        post = get_object_or_404(Post.objects.select_related('autor'), id=id, status='publicado')

    return render(request, 'blog/detalhe.html', {'post': post})


@login_required
def criar_post(request):
    perfil = _obter_perfil(request.user)
    if perfil is None:
        return HttpResponseForbidden('Usuário sem perfil de funcionário associado a uma página.')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.pagina = perfil.pagina
            post.save()
            messages.success(request, 'Matéria salva com sucesso.')
            return redirect('detalhe', id=post.id)
    else:
        form = PostForm()

    return render(request, 'blog/form.html', {'form': form})


@login_required
def editar_post(request, id):
    perfil = _obter_perfil(request.user)
    if perfil is None:
        return HttpResponseForbidden('Usuário sem perfil de funcionário associado a uma página.')

    post = get_object_or_404(Post, id=id, pagina=perfil.pagina)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matéria atualizada com sucesso.')
            return redirect('detalhe', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/form.html', {'form': form, 'post': post})


@login_required
def excluir_post(request, id):
    perfil = _obter_perfil(request.user)
    if perfil is None:
        return HttpResponseForbidden('Usuário sem perfil de funcionário associado a uma página.')

    post = get_object_or_404(Post, id=id, pagina=perfil.pagina)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Matéria excluída com sucesso.')
        return redirect('lista')

    return render(request, 'blog/excluir.html', {'post': post})


@login_required
def dashboard_view(request):
    perfil = _obter_perfil(request.user)
    if perfil is None:
        return HttpResponseForbidden('Usuário sem perfil de funcionário associado a uma página.')

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
    perfil = _obter_perfil(request.user)
    if perfil is None or not perfil.eh_admin:
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


def sair_view(request):
    logout(request)
    return redirect('/admin/login/?next=/')