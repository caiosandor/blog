from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostListCreate(generics.ListCreateAPIView):
    # GET lista todos os posts, POST cria um novo post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # GET detalha, PUT/PATCH atualiza, DELETE apaga
    queryset = Post.objects.all()
    serializer_class = PostSerializer