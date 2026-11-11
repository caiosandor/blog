from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer

@login_required
def lista_posts(request):
    # Lista apenas os posts vinculados a pagina do usuario logado
    posts = Post.objects.filter(pagina=request.user.perfilfuncionario.pagina)
    
    # Captura os parametros de filtro passados na URL
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
        # Exibe os posts publicados caso nenhum filtro seja aplicado
        posts = posts.filter(status='publicado')

    return render(request, 'blog/lista.html', {'posts': posts})

@login_required
def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Prepara o objeto sem salvar no banco ainda
            post = form.save(commit=False)
            # Injeta o autor e a pagina do usuario logado
            post.autor = request.user
            post.pagina = request.user.perfilfuncionario.pagina
            post.save()
            return redirect('lista')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {'form': form})

@login_required
def post_detalhe(request, id):
    # Busca o post garantindo a trava de seguranca por pagina
    post = get_object_or_404(Post, id=id, pagina=request.user.perfilfuncionario.pagina)
    return render(request, 'blog/detalhe.html', {'post': post})

@login_required
def lista_rascunhos(request):
    # Filtra os rascunhos vinculados a pagina do usuario
    rascunhos = Post.objects.filter(pagina=request.user.perfilfuncionario.pagina, status='rascunho')
    return render(request, 'blog/rascunhos.html', {'posts': rascunhos})

@login_required
def editar_post(request, id):
    # Busca o post para edicao mantendo o isolamento por pagina
    post = get_object_or_404(Post, id=id, pagina=request.user.perfilfuncionario.pagina)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalhe', id=post.id)
    else:
        form = PostForm(instance=post)
    
    # Renderiza o formulario passando a instancia para preencher os dados
    return render(request, 'blog/form.html', {'form': form, 'post': post})

@login_required
def excluir_post(request, id):
    # Busca o post para exclusao mantendo o isolamento por pagina
    post = get_object_or_404(Post, id=id, pagina=request.user.perfilfuncionario.pagina)
    if request.method == 'POST':
        post.delete()
        return redirect('lista')
    return render(request, 'blog/excluir.html', {'post': post})

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfilfuncionario'):
            # Retorna no GET da API apenas os posts da pagina do usuario
            return Post.objects.filter(pagina=user.perfilfuncionario.pagina)
        # Retorna uma lista vazia se o usuario nao tiver perfil vinculado
        return Post.objects.none() 

    def perform_create(self, serializer):
        # Injeta os dados sensiveis no POST da API antes de criar o registro
        serializer.save(
            autor=self.request.user, 
            pagina=self.request.user.perfilfuncionario.pagina
        )