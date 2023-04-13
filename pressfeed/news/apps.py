from django.apps import AppConfig
import os


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # I have created this ready function to ensure my scheduler from news/tasks.py is started when the news app has
    def ready(self):
        if (os.environ.get('RUN_MAIN') or os.environ.get('DEBUG') == 'False'):
            from .tasks import start_scheduler
            start_scheduler()

            from .news_scraper import update_news
            update_news()

