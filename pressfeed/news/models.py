from django.db import models

# Create your models here.

#Source of articles model
class Source(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)

    def __str__(self):
        return self.name

#Articles model
class Articles(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField(max_length=2048)
    published_at = models.DateTimeField(null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return self.title


