from django.shortcuts import render
from .models import Article
import environ
import requests
import json
import time


env = environ.Env()
environ.Env.read_env()

def home(request):

    return render(request, 'home.html', {})

def testfeed(request):

    # use NewsAPI call to fetch article data
    # start = time.time()
    # irish_news_request = requests.get(f'https://newsapi.org/v2/top-headlines?country=ie&apiKey={env("NEWSAPI_KEY")}')
    # newsapi_response = json.loads(irish_news_request.content)
    # end = time.time()
    # print(f'TIME TO CALL API: {end - start}')
    # return render(request, 'testfeed.html', {'api': newsapi_response})

    #use PostgreSQL Article model to fetch article data
    articles = Article.objects.order_by('-published_at')
    return render(request, 'testfeed.html', {'articles': articles})