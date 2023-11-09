from celeryworker.celery import app
from celery.schedules import crontab
from celery import shared_task

from . import services, models


# currently gets description for three closest days, including today
# but weather is for 5 days
@app.task
def task_get_weather():
    print('task started')
    services.get_weather()


@app.task
def task_update_weather_time(time):
    print('task started')
    create_schedule(time)


def create_schedule(time):
    if time:
        hour, minute = time.hour, time.minute
    else:
        time = models.WeatherUpdateSettings.objects.get(id=1).time
        hour, minute = time.hour, time.minute
    schedule = crontab(minute=minute, hour=hour)
    app.conf.beat_schedule = {
        "regular-weather-update": {
            "task": "weather.tasks.task_get_weather",
            "schedule": schedule,
        }

    }


# create_schedule("")

@app.task
def task_update_schedule(time):
    pass