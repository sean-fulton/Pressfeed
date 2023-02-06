import requests
import json
from celery import task

@task
def update_news():
    retrieve_news()

def retrieve_news():
    # Call NewsAPI v2 endpoint to scrape News data
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey=your_api_key={env("NEWSAPI_KEY")}')

    # verify request success
    if response.status_code == 200:
        # parse response
        data = json.loads(response.content)

        for article in data["articles"]:
            title = article["title"]
            description = article["description"]
            url = article["url"]
            published_at = article["publishedAt"]

            Article.objects.create(
                title=title,
                description=description,
                url=url,
                published_at=published_at
            )