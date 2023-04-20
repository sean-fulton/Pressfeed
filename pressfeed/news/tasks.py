import threading
from . news_scraper import update_news
import schedule
import time

def start_scheduler():
    def scheduler():
        #Wait for db migrations to pass before executing
        time.sleep(10)
        # Schedule update_news every 4 hours
        schedule.every(4).hours.do(update_news)
        #initial call at app startup to update news
        update_news()
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
