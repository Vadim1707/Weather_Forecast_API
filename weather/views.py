from rest_framework.response import Response
from rest_framework import viewsets, mixins
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from celery.result import AsyncResult

from datetime import datetime, timedelta

from . import models, serializers, tasks
# Create your views here.


class WeatherGetViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.KyivWeatherSerializer
    queryset = models.KyivWeather.objects.all()

    def get_queryset(self):
        today = datetime.now()
        return models.KyivWeather.objects.filter(date__gte=today, date__lte=today+timedelta(days=5))


class WeatherTaskViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = serializers.WeatherTaskStatusSerializer
    queryset = models.WeatherTask.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.data)
        task = tasks.task_get_weather.delay()
        # print(serializer.validated_data['city'])
        task_id = str(task.id)

        weather_task = models.WeatherTask.objects.create(
            celery_id=task_id,
            status=task.status
        )

        return Response(model_to_dict(weather_task))

    def retrieve(self, request, *args, **kwargs):
        _id = kwargs['pk']

        weather_task = get_object_or_404(models.WeatherTask, pk=_id)
        result_ = AsyncResult(id=weather_task.celery_id, task_name=tasks.task_get_weather)

        weather_task.status = result_.status
        weather_task.save()

        serializer = self.serializer_class(weather_task)
        return Response(serializer.data)


class WeatherSettingsView(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = serializers.WeatherSettingsSerializer
    queryset = models.WeatherUpdateSettings.objects.all()

    def update(self, request, *args, **kwargs):
        _id = kwargs['pk']
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.data)

        weather_settings = get_object_or_404(models.WeatherUpdateSettings, pk=_id)
        weather_settings.time = serializer.validated_data['time']
        weather_settings.save()

        tasks.create_schedule(weather_settings.time)

        return Response(self.serializer_class(weather_settings).data)


