import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geodjango.settings')

app = Celery('geodjango')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
