# celery config
from celery import Celery
from celery.schedules import crontab

#Create Celery associations
app = Celery('pressfeed')
app.config_from_object('django.conf:settings', namespace='CELERY')

#cron job to call update news everyday at 7:00am
CELERY_BEAT_SCHEDULE = {
    'update_news_daily': {
        'task': 'path.to.update_news',
        'schedule': crontab(hour=7, minute=0),
    },
}
