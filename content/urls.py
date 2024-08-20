from django.urls import path
from .views import NewsArticleListCreateView, NewsArticleDetailView

urlpatterns = [
    path('news/', NewsArticleListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsArticleDetailView.as_view(), name='news-detail'),
]
