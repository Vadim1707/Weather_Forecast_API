import datetime

from django.db import models

# Create your models here.


class KyivWeather(models.Model):
    temperature = models.SmallIntegerField(verbose_name='Temperature')
    date = models.DateField(primary_key=True, verbose_name='Date')
    description = models.CharField(max_length=150, verbose_name='Description')

    def __str__(self):
        return f"{self.date}, temp: {self.temperature}, desc: {self.description}"

    class Meta:
        verbose_name = 'Weather'
        verbose_name_plural = 'Weather'


class WeatherTask(models.Model):
    class Status(models.TextChoices):
        PENDING = ("PENDING", "PENDING")
        STARTED = ("STARTED", "STARTED")
        SUCCESS = ("SUCCESS", "SUCCESS")
        FAILURE = ("FAILURE", "FAILURE")
        RETRY = ("RETRY", "RETRY")
        REVOKED = ("REVOKED", "REVOKED")

    celery_id = models.CharField(max_length=36, verbose_name='Celery id')
    status = models.CharField(choices=Status.choices, max_length=100, default=Status.PENDING, verbose_name='Status')

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = 'Weather status'
        verbose_name_plural = 'Weather statuses'


class WeatherUpdateSettings(models.Model):

    time = models.TimeField(verbose_name='Update time')

    def __str__(self):
        return str(self.time)

    class Meta:
        default_permissions = ('change', 'view')
        verbose_name = 'Weather settings'
        verbose_name_plural = 'Weather settings'


# WeatherUpdateSettings.objects.create(time=datetime.time(hour=9))
