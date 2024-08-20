from django.db import models
from django.conf import settings

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    LINK = models.TextField(default='')
    category = models.CharField(max_length=200,default='')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/', null=False, blank=False,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
