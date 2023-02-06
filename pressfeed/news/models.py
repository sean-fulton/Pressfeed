from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    published_at = models.DateTimeField()


