from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.

#Source of articles model
class Source(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)
    subscribers = models.ManyToManyField(User, related_name='sources')

    def __str__(self):
        return self.name

#Article model
class Article(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True)
    url = models.URLField(max_length=2048)
    published_at = models.DateTimeField(null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_comment_count(self):
        return self.comments.count()
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_dislikes_count(self):
        return self.dislikes.count()

#Comment model

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"
    
    def is_author(self, user):
        return self.user == user
    
    def edit(self, text):
        self.text = text
        self.modified_at = timezone.now()

    def delete(self, *args, **kwargs):
        super(Comment, self).delete(*args, **kwargs)
    
#Like model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name="unique_like")
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"


#Dislike model
class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name="unique_dislike")
        ]

    def __str__(self):
        return f"{self.user.username} dislikes {self.article.title}"