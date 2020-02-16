from __future__ import absolute_import,unicode_literals
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from weather.models import City
@periodic_task(run_every=(crontab(minute='*/1')),name="get_new_cities")
def get_new_cities():

    '''Task for getting new cities in DB from user settings. Runs every minute.'''

    City.objects.get_new_cities()

@periodic_task(run_every=(crontab(minute='*/60')),name="get_weather_from_openweatherapi")
def get_weather_from_openweatherapi():
    '''Task for getting weather from OpenWeatherAPI for cities in DB. Write Result into weather table in DB. Runs every hour. '''

    City.objects.get_weather_from_openweatherapi()

@periodic_task(run_every=(crontab(minute='*/60')),name="get_weather_from_weatheronline")
def get_weather_from_weatheronline():
    '''Task for getting weather from WeatherOnline for cities in DB. Write Result into weather table in DB. Runs every hour. '''

    City.objects.get_weather_from_weatheronline()

@periodic_task(run_every=(crontab(minute='*/60')),name="get_weather_from_weatherapi")
def get_weather_from_weatherapi():

    '''Task for getting weather from WeatherAPI for cities in DB. Write Result into weather table in DB.  Runs every hour.'''

    City.objects.get_weather_from_weatherapi()

