from django.urls import path
from . import views, api_views

urlpatterns = [
    # Rotas das views HTML do blog
    path('', views.lista_posts, name='lista'),
    path('novo/', views.criar_post, name='criar'),
    path('rascunhos/', views.lista_rascunhos, name='rascunhos'),
    path('post/<int:id>/', views.post_detalhe, name='detalhe'),
    path('post/<int:id>/editar/', views.editar_post, name='editar'),
    path('post/<int:id>/excluir/', views.excluir_post, name='excluir'),

    # Rotas do dashboard e exportação de relatórios
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/exportar-csv/', views.exportar_posts_csv, name='exportar-posts-csv'),

    # Rotas da API REST
    path('api/posts/', api_views.PostListCreate.as_view(), name='api-post-list'),
    path('api/posts/<int:pk>/', api_views.PostDetail.as_view(), name='api-post-detail'),
    path('api/dashboard/', api_views.DashboardAPIView.as_view(), name='api-dashboard'),
]