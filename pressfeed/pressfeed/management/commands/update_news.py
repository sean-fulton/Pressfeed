from django.core.management.base import BaseCommand
from news import news_scraper


class Command(BaseCommand):
    help = 'Triggers the update_news task'

    def handle(self, *args, **kwargs):
        news_scraper.update_news()
        self.stdout.write(self.style.SUCCESS('update_news triggered successfully'))
