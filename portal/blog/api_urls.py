from django.urls import path
from .api_views import PostListCreate, PostDetail

urlpatterns = [
    path('posts/', PostListCreate.as_view(), name='api-post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='api-post-detail'),
]