from django.shortcuts import render
from newsapi import NewsApiClient
import environ

env = environ.Env()
environ.Env.read_env()

def home(request):
    import requests
    import json

    # top_irish_christmas_headlines = newsapi.get_top_headlines(q='Christmas',
    #                                                           language='en',
    #                                                           country='ie')

    irish_news_request = requests.get(f'https://newsapi.org/v2/top-headlines?country=ie&{env("NEWSAPI_KEY")}')
    newsapi_response = json.loads(irish_news_request.content)

    return render(request, 'home.html', {'api': newsapi_response})