import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'newsletter_about_creating_post': {
        'task': 'news.tasks.newsletter_every_week',
        'schedule': crontab(hour=18, minute=27, day_of_week='wed'),
        'args': ()
    },
}

app.conf.timezone = 'CET'