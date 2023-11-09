from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.KyivWeather)
admin.site.register(models.WeatherTask)
admin.site.register(models.WeatherUpdateSettings)
