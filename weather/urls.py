from django.urls import path, include
from rest_framework import routers
from . import views

weather_view = routers.SimpleRouter()
weather_view.register("weather", views.WeatherGetViewSet)
weather_update_status_view = routers.SimpleRouter()
weather_update_status_view.register("weather update", views.WeatherTaskViewSet)
weather_settings_view = routers.SimpleRouter()
weather_settings_view.register("weather settings", views.WeatherSettingsView)

urlpatterns = (

    weather_view.urls +
    weather_settings_view.urls +
    weather_update_status_view.urls
    # [path("weather/", include(weather_view.urls), name='weather')] +
    # [path("weather status/", include(weather_update_status_view.urls), name='weather status')] +
    # [path("weather settings", include(weather_settings_view.urls), name='weather settings')]

)
