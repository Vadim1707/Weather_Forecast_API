import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from . import models
# Create your tests here.


class WeatherTest(TestCase):
    def setUp(self) -> None:
        self.first_weather = models.KyivWeather.objects.create(
            description="weather",
            temperature=10,
            date=datetime.datetime.now()
        )

        self.weather_update = models.WeatherUpdateSettings.objects.create(
            time=datetime.time(minute=0, hour=9)
        )

    def test_user_can_get_weather(self):
        url = 'http://127.0.0.1:8000/api/weather/'
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)

    def test_weather(self):
        url = 'http://127.0.0.1:8000/api/weather/'
        response = self.client.delete(path=url, data={'id': 1})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        url = f"http://127.0.0.1:8000/api/weather/"
        body = {'description': '',
                'temperature': 10,
                'date': self.first_weather.date
                }
        response = self.client.put(path=url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        url = 'http://127.0.0.1:8000/api/weather/'
        response = self.client.patch(path=url, data={'id': 1})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_can_update_schedule(self):
        # Patch
        url = f"http://127.0.0.1:8000/api/weather settings/{self.weather_update.id}/"
        body = {'time': datetime.time(hour=10)}
        response = self.client.patch(path=url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['time'], "10:00:00")

        # Put
        url = f"http://127.0.0.1:8000/api/weather settings/{self.weather_update.id}/"
        body = {'time': datetime.time(hour=8)}
        response = self.client.put(path=url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['time'], "08:00:00")

    # doesn't work now
    # def test_can_manually_schedule_weather(self):
    #     url = "http://0.0.0.0:8000/api/weather update/"
    #     body = {"status": "PENDING"}
    #     response = self.client.post(path=url, data=body, content_type="application/json")
    #
    #     self.assertNotEqual(len(response.data), 0)
    #
    #     weather_forecasts = models.KyivWeather.objects.all().count()
    #     self.assertEqual(weather_forecasts, 6)
