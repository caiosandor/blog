from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from .forms import filtrar_periodo
from .dashboard import obter_metricas_dashboard


class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(
            pagina=user.perfilfuncionario.pagina
        ).select_related('autor')

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(autor=user, pagina=user.perfilfuncionario.pagina)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(
            pagina=user.perfilfuncionario.pagina
        ).select_related('autor')


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Reutiliza a camada de métricas e o filtro de período da interface web
        minha_pagina = request.user.perfilfuncionario.pagina
        base_qs = Post.objects.filter(pagina=minha_pagina)
        qs_filtrada, _ = filtrar_periodo(request, base_qs)

        metricas = obter_metricas_dashboard(minha_pagina, qs_posts=qs_filtrada)

        return Response({
            "pagina": minha_pagina.nome,
            **metricas,
        })