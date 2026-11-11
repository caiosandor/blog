from django.urls import path
from . import api_views

urlpatterns = [
    path('api/posts/', api_views.PostListCreate.as_view(), name='api-post-list'),
    path('api/posts/<int:pk>/', api_views.PostDetail.as_view(), name='api-post-detail'),
    
    # Endpoint que devolve os dados agregados para o dashboard
    path('api/dashboard/', api_views.DashboardAPIView.as_view(), name='api-dashboard'),
]