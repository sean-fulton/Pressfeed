from news.news_scraper import update_news
import schedule
import time

def run_scheduler():
    # Schedule update_news every 4 hours
    schedule.every(4).hours.do(update_news)

    while True:
        schedule.run_pending()
        time.sleep(1)
