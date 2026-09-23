from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post
from .forms import PostForm

def lista_posts(request):
    posts = Post.objects.all()
    
    # Feature 1 P1: Captura os parâmetros da URL para filtro e busca
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
        # Padrão: mostra apenas publicados se não houver filtro
        posts = posts.filter(status='publicado')

    return render(request, 'blog/lista.html', {'posts': posts})

def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {'form': form})

def post_detalhe(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/detalhe.html', {'post': post})

def lista_rascunhos(request):
    rascunhos = Post.objects.filter(status='rascunho')
    return render(request, 'blog/rascunhos.html', {'posts': rascunhos})

# --- NOVAS VIEWS PARA COMPLETAR O CRUD ---

def editar_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalhe', id=post.id)
    else:
        form = PostForm(instance=post)
    
    # Reaproveita o form.html, passando o 'post' para a view saber que é edição
    return render(request, 'blog/form.html', {'form': form, 'post': post})

def excluir_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('lista')
    return render(request, 'blog/excluir.html', {'post': post})





