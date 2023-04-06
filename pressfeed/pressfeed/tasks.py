from news.news_scraper import update_news
import schedule
import time

def run_scheduler():
    schedule.every(4).hours.do(update_news)

    while True:
        schedule.run_pending()
        time.sleep(1)
