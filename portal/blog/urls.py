from django.urls import path
from . import api_views

urlpatterns = [
    # Rotas da API RESTful
    path('api/posts/', api_views.PostListCreate.as_view(), name='api-post-list'),
    path('api/posts/<int:pk>/', api_views.PostDetail.as_view(), name='api-post-detail'),
]