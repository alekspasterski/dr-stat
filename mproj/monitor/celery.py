#!/usr/bin/env python3

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitor.settings')

app = Celery('monitor')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
