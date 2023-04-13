import threading
from . news_scraper import update_news
import schedule
import time

lock = threading.Lock()
scheduler_started = False

def start_scheduler():
    global scheduler_started
    if(scheduler_started):
        return

    scheduler_started = True

    def scheduler():
        # Schedule update_news every 4 hours
        schedule.every(4).hours.do(update_news)
        with lock:
            update_news()

        while True:
            with lock:
                schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
