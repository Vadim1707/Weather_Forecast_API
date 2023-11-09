import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("Django_settings_module", "WeatherForTodayProject.settings")
app = Celery("celeryworker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()




