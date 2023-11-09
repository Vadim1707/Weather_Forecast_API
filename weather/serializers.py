from rest_framework import serializers
from . import models


class KyivWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KyivWeather
        fields = "__all__"
        read_only_fields = models.KyivWeather._meta.fields


class WeatherTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeatherTask
        fields = "__all__"
        read_only_fields = ('celery_id', )


class WeatherSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeatherUpdateSettings
        fields = "__all__"

