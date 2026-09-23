from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.lista_posts, name='lista'),
    path('posts/novo/', views.criar_post, name='criar_post'),
    path('posts/<int:id>/', views.post_detalhe, name='detalhe'),
    path('rascunhos/', views.lista_rascunhos, name='rascunhos'),
    path('posts/<int:id>/editar/', views.editar_post, name='editar'),
    path('posts/<int:id>/excluir/', views.excluir_post, name='excluir'),
]