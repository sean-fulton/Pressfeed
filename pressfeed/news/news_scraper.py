import requests
import json
import environ
from .models import Source
from .models import Article
from django.db.utils import IntegrityError

# from google.cloud import firestore

# db = firestore.Client()

env = environ.Env()
environ.Env.read_env()


def update_news():
    news_data = retrieve_news()
    store_news(news_data)


def retrieve_news():
    # Call NewsAPI v2 endpoint to scrape News data
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=ie&apiKey={env("NEWSAPI_KEY")}')
    # verify request success
    if response.status_code == 200:
        return response.json()


def store_news(news_data):
    for article in news_data['articles']:
        if (article['title'] is not None) and (article['description'] is not None) and (article['url'] is not None):
            try:

                source, created = Source.objects.get_or_create(
                    name=article['source']['name']
                )

                article_obj, created = Article.objects.get_or_create(
                    title=article['title'],
                    description=article['description'],
                    url=article['url'],
                    published_at=article['publishedAt'],
                    source=source,
                    thumbnail_url=article['urlToImage']
                )
            except IntegrityError:
                # Ignore duplicate article entries
                pass

