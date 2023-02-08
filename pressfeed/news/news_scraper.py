import requests
import json
import environ
from google.cloud import firestore

db = firestore.Client()

env = environ.Env()
environ.Env.read_env()

def update_news():
    news_data = retrieve_news()
    store_news(news_data)

def retrieve_news():
    # Call NewsAPI v2 endpoint to scrape News data
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={env("NEWSAPI_KEY")}')
    # verify request success
    if response.status_code == 200:
        return response.json()

def store_news(news_data):
    for article in news_data['articles']:
        news_ref = db.collection(u'news').document()
        news_ref.set({
            u'title': article['title'],
            u'description': article['description'],
            u'url': article['url'],
            u'published_at': article['publishedAt'],
            u'source': {
                u'id': article['source']['id'],
                u'name': article['source']['name']
            }
        })