from django.shortcuts import render
from news.models import Article

def home(request):
    articles = Article.objects.order_by('-published_at')[:4]

    if request.user.is_authenticated:
        user = request.user

        for article in articles:
            article.has_liked = article.likes.filter(user=user).exists()
            article.has_disliked = article.dislikes.filter(user=user).exists()
    
    return render(request, 'home.html', {'articles': articles})