import threading
from . news_scraper import update_news
import schedule
import time

def start_scheduler():
    def run_scheduler():
        # Schedule update_news every 4 hours
        schedule.every(10).seconds.do(update_news)

        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
