from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Source
from pressfeed.forms import SubscriptionForm
import environ
import requests
import json
import time

env = environ.Env()
environ.Env.read_env()


def home(request):
    return render(request, 'home.html', {})


@login_required
def subscribe(request):
    sources = Source.objects.all()

    # If form submitted and valid, process subscription/unsubscription
    if request.method == 'POST':
        for source in sources:
            if source.name in request.POST:
                # If source is checked and user is not subscribed, subscribe user
                print(request.POST.get(source.name))
                if request.POST.get(source.name) == 'on':
                    source.subscribers.add(request.user)
                # If source is unchecked and user is subscribed, unsubscribe user
            elif request.POST.get(source.name) == None:
                    source.subscribers.remove(request.user)

        return redirect('subscribe')

    # If no form submitted, show user's subscribed sources
    user_sources = request.user.sources.all()
    return render(request, 'subscribe.html', {'sources': sources, 'user_sources': user_sources})

def testfeed(request):
    # use NewsAPI call to fetch article data
    # start = time.time()
    # irish_news_request = requests.get(f'https://newsapi.org/v2/top-headlines?country=ie&apiKey={env("NEWSAPI_KEY")}')
    # newsapi_response = json.loads(irish_news_request.content)
    # end = time.time()
    # print(f'TIME TO CALL API: {end - start}')
    # return render(request, 'testfeed.html', {'api': newsapi_response})

    # use PostgreSQL Article model to fetch article data
    articles = Article.objects.order_by('-published_at')
    return render(request, 'testfeed.html', {'articles': articles})

@login_required
def newsfeed(request):
    user = request.user
    sources = user.sources.all()
    articles = Article.objects.filter(source__in=sources).order_by('-published_at')
    return render(request, 'newsfeed.html', {'articles': articles})

