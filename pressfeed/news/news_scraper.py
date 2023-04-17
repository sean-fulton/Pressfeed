import requests
import json
import environ
from .models import Source
from .models import Article
import datetime
from django.db.utils import IntegrityError

env = environ.Env()
environ.Env.read_env()


# Simple method to encapsulate the logic of both retieve news and store news to be called by the scheduler / managment command
def update_news():
    irish_news_data = retrieve_news('ie')
    store_news(irish_news_data)

    us_news_data = retrieve_news('us')
    store_news(us_news_data)
    
    uk_news_data = retrieve_news('gb')
    store_news(uk_news_data)

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Updated News at " + formatted_date)


# Calls NewsAPI top-headlines endpoint to scrape news data based on the country param
def retrieve_news(country):
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={env("NEWSAPI_KEY")}')
    # verify request success
    if response.status_code == 200:
        return response.json()


# Persists news data from a json object to the article and source models
def store_news(news_data):
    if news_data is not None and 'articles' in news_data:
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
    else:
        return
