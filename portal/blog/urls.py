from django.urls import path
from . import views

urlpatterns = [
    # Rotas de interface web (templates HTML)
    path('', views.lista_posts, name='lista'),
    path('novo/', views.criar_post, name='criar_post'),
    path('rascunhos/', views.lista_rascunhos, name='rascunhos'),
    path('post/<int:id>/', views.post_detalhe, name='detalhe'),
    path('post/<int:id>/editar/', views.editar_post, name='editar'),
    path('post/<int:id>/excluir/', views.excluir_post, name='excluir'),

    # Rotas do dashboard gerencial e exportação CSV
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/exportar-csv/', views.exportar_posts_csv, name='exportar-posts-csv'),

    # Rota de encerramento de sessão
    path('sair/', views.sair_view, name='logout'),
]