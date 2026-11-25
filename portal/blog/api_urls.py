from django.urls import path
from . import api_views

urlpatterns = [
    # Endpoints da API REST (JSON)
    path('api/posts/', api_views.PostListCreate.as_view(), name='api-post-list'),
    path('api/posts/<int:pk>/', api_views.PostDetail.as_view(), name='api-post-detail'),
    path('api/dashboard/', api_views.DashboardAPIView.as_view(), name='api-dashboard'),
]