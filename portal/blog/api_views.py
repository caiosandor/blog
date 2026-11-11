from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import Post
from .serializers import PostSerializer

class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    # Trava a API para aceitar apenas usuários logados
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        # Isola os dados: retorna apenas os posts da página que o funcionário logado pertence
        user = self.request.user
        return Post.objects.filter(pagina=user.perfilfuncionario.pagina)

    def perform_create(self, serializer):
        # Injeta automaticamente o autor e a página do usuário na hora de salvar o post
        user = self.request.user
        serializer.save(autor=user, pagina=user.perfilfuncionario.pagina)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Reaproveita o filtro para impedir que alguém acesse ou exclua um post de outra página passando o ID na URL
        user = self.request.user
        return Post.objects.filter(pagina=user.perfilfuncionario.pagina)

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        minha_pagina = request.user.perfilfuncionario.pagina
        
        # Levanta a quantidade de posts agrupados por status (ex: x publicados, y rascunhos)
        metricas_status = (
            Post.objects
            .filter(pagina=minha_pagina)
            .values('status')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        
        return Response({
            "pagina": minha_pagina.nome,
            "posts_por_status": metricas_status
        })