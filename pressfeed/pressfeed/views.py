from django.shortcuts import render, redirect
from news.models import Article

def home(request):

    articles = Article.objects.order_by('-published_at')[:4]
    return render(request, 'home.html', {'articles': articles})