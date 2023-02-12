from django.shortcuts import render
from .models import Article
import environ
import requests
import json


env = environ.Env()
environ.Env.read_env()

def home(request):

    # top_irish_christmas_headlines = newsapi.get_top_headlines(q='Christmas',
    #                                                           language='en',
    #                                                           country='ie')

    # irish_news_request = requests.get(f'https://newsapi.org/v2/top-headlines?country=ie&apiKey={env("NEWSAPI_KEY")}')
    # newsapi_response = json.loads(irish_news_request.content)

    articles = Article.objects.all()
    return render(request, 'home.html', {'articles': articles})