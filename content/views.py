from rest_framework import generics
from .models import NewsArticle
from .serializers import NewsArticleSerializer

# Vista para listar y crear artículos de noticias
class NewsArticleListCreateView(generics.ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

# Vista para recuperar, actualizar y eliminar un artículo de noticias específico
class NewsArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
