from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookingProject.settings')

app = Celery('bookingProject')
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'check-room-availability-every-minute': {
        'task': 'bookingApp.tasks.reset_availability',  
        'schedule': 60.0,   
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Paris'


app.autodiscover_tasks()

