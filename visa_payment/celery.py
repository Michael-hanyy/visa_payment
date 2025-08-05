import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visa_payment.settings')

app = Celery('visa_payment')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
