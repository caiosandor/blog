from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.lista_posts, name='lista'),
    path('posts/novo/', views.criar_post, name='criar_post'),
    path('posts/<int:id>/', views.post_detalhe, name='detalhe'),
    path('rascunhos/', views.lista_rascunhos, name='rascunhos'), # Nova rota do formulário
]