import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

celery_app = Celery('application')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.enable_utc = False
