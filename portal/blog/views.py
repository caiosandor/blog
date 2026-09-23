from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

def lista_posts(request):
    posts = Post.objects.filter(status='publicado')
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
    # Busca apenas os posts que estão como rascunho
    rascunhos = Post.objects.filter(status='rascunho')
    return render(request, 'blog/rascunhos.html', {'posts': rascunhos})