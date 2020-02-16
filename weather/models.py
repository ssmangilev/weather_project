from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
import requests
import re

CONST_CITIES='London,Paris,Berlin,Barcelona,Bonn,Moscow,Samara'# Cities string for noauth users and for auth users, when favorites_cities is None. 
# Create your models here.

#Creating custom User model
class CustomUserManager (UserManager):

   '''Manager class for CustomUser model.  '''

   def get_weather_favorite_cities_auth_users(self,pk):

      '''Function check auth and settings of auth users and get weather from personal list. '''

      all_cities_first_api=[]
      all_cities_second_api=[]
      all_cities_third_api=[]
      favorite_cities=CustomUser.objects.get(pk=pk).favorite_cities # Get favorite cities users list.
      if favorite_cities: # Check that favorite_cities is not None.
         cities=favorite_cities.split(",") # Get list from string.
      else: 
         cities = CONST_CITIES.split(",") # Popular cities for all users.
      for i in cities:
         if CustomUser.objects.get(pk=pk).open_weather_map: # Check settings in user profile , and if checkbox is True, get last record from database for this API.
            res = Weather.objects.filter(city_name=i,API_NAME='openweatherAPI').order_by('-date_of_getting').first()
            if res.ERROR !='': # Check what city is real.
                  city_info={
                     'city':i,
                     'message':res.ERROR
                  }
                  all_cities_first_api.append(city_info)
                  continue
            city_info={
               'city':i, #Get city_name.
               'temp':res.temperature, #Get temp.
               'icon':res.icon #Get icon.
            }
            all_cities_first_api.append(city_info)
         if CustomUser.objects.get(pk=pk).world_weather_online: # Check settings in user profile , and if checkbox is True, get last record from database for this API.
            res = Weather.objects.filter(city_name=i,API_NAME='worldweatheronlineAPI').order_by('-date_of_getting').first()
            if res.ERROR !='': # Check what city is real.
                  city_info={
                     'city':i,
                     'message':res.ERROR
                  }
                  all_cities_second_api.append(city_info)
                  continue
            city_info={
               'city':i, #Get city_name.
               'temp':res.temperature, #Get temp.
               'icon':res.icon #Get icon.
            }
            all_cities_second_api.append(city_info)
         if CustomUser.objects.get(pk=pk).weather_api: # Check settings in user profile , and if checkbox is True, get last record from database for this API.
            res = Weather.objects.filter(city_name=i,API_NAME='weatherAPI').order_by('-date_of_getting').first()
            if res.ERROR !='': # Check what city is real.
                  city_info={
                     'city':i,
                     'message':res.ERROR
                  }
                  all_cities_third_api.append(city_info)
                  continue
            city_info={
               'city':i, #Get city_name.
               'temp':res.temperature, #Get temp.
               'icon':res.icon #Get icon.
            }
            all_cities_third_api.append(city_info)
      return all_cities_first_api,all_cities_second_api,all_cities_third_api    # Return cities list with data.
   def get_weather_favorite_cities_notauth_users(self):

      '''Function gets weather for noauth users from CONST_CITIES, used only one API. '''

      all_cities=[]
      cities = CONST_CITIES.split(",")
      for i in cities:
         res = Weather.objects.filter(city_name=i,API_NAME='openweatherAPI').order_by('-date_of_getting').first() # Check settings in user profile , and if checkbox is True, get last record from database for this API.
         if res.ERROR !='': # Check what city is real.
            city_info={
                     'city':i,
                     'message':res.ERROR
                     }
            all_cities.append(city_info)
            continue
         else:
            city_info={
               'city':i, #Get city_name.
               'temp':res.temperature, #Get temp.
               'icon':res.icon #Get icon.
            }
            all_cities.append(city_info)
      return all_cities # Return cities list with data.
         
class CustomUser(AbstractUser):

   '''Class for CustomUser model. '''

   open_weather_map = models.BooleanField(default=True)
   world_weather_online=models.BooleanField(default=False)
   weather_api = models.BooleanField(default=False)
   favorite_cities = models.CharField(max_length=4000,blank=True)
   objects = CustomUserManager()
   def get_absolute_url(self):

      '''Function for getting url with user_id '''

      return reverse ('profile_url',args=[self.pk])

class CityManager(models.Manager):

   '''Manager class for City model. '''

   def get_new_cities(self): 

      '''Function for insert new_cities in weather_city table'''

      users = CustomUser.objects.all() # Get all user.objects.
      list1 = []
      c_favorite_cities = CONST_CITIES.split(",")
      for c in c_favorite_cities:
         list1.append(c)
      for user in users: 
         for item in user.favorite_cities.split(","): # Get user.favorite_cities.
            if item=='': # Check when favorite_cities not None
               continue
            else:
               #print(item)
                  #item[0]=re.sub(' ','',item) # need check only first symbol
               list1.append(item) # Adding city on list.
      clear_list=list(set(list1)) # Delete duplicates .
      for city_name in clear_list: # Adding city into weather_city table.
         try:
            city = City.objects.get(city_name=city_name)
         except:
            new_city=City(city_name=city_name)
            new_city.save()

   def get_weather_from_openweatherapi(self):

      '''Function for getting weather from OpenWeatherAPI. '''

      open_weather_map_api_key = '68b12f971d6b5bb4fbf4c5239217920e'
      url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+open_weather_map_api_key #Get correct api url.
      city_objects = City.objects.all() # Get all city objects.
      for city in city_objects:
         res=requests.get(url.format(city.city_name)).json() # Get response from API. 
         if res.get('message')=='city not found': # Check errors.
            city_weather=Weather(city_name=city.city_name,ERROR=res.get('message'),API_NAME='openweatherAPI')
            city_weather.save()
         else:
            city_weather=Weather(city_name=city.city_name,temperature=res["main"]["temp"],icon=res["weather"][0]["icon"],
            API_NAME='openweatherAPI')
            city_weather.save() # Save Result in DB.
   def get_weather_from_weatheronline(self):

      '''Function for getting weather from WeatherOnline. '''

      world_weather_online_key='a48fa20f6ca14616865142928200801'
      url='https://api.worldweatheronline.com/premium/v1/weather.ashx?key='+world_weather_online_key+'&q={}&format=json' # Get correct API url.
      city_objects = City.objects.all()  # Get all city objects.
      for city in city_objects:
         res = requests.get(url.format(city.city_name)).json # Get response from API.
         if res()['data'].get('error'): # Check errors.
            city_weather = Weather (city_name=city.city_name,ERROR=res()['data'].get('error')[0].get('msg'),API_NAME='worldweatheronlineAPI')
            city_weather.save()
         else:
            city_weather=Weather(city_name=city.city_name,temperature=res()['data']['current_condition'][0].get('temp_C'),icon=res()['data']['current_condition'][0]['weatherIconUrl'][0].get('value'),
            API_NAME='worldweatheronlineAPI')
            city_weather.save() # Save result in DB.

   def get_weather_from_weatherapi(self):

      '''Function for getting weather from WeatherAPI. '''

      weather_api_key = '09d4b44352f946a0ba6142526200801'
      url = 'https://api.weatherapi.com/v1/current.json?key='+weather_api_key+'&q={}' # Get correct API url.
      city_objects = City.objects.all() # Get all city objects.
      for city in city_objects:
         res = requests.get(url.format(city.city_name)).json() # Get response from API.
         if not res.get('error') is None: # Check errors.
            city_weather = Weather (city_name=city.city_name,ERROR=res['error']['message'],API_NAME='weatherAPI')
            city_weather.save()
         else:
            city_weather = Weather(city_name=city.city_name,temperature=res['current']['temp_c'],icon='https:'+res['current']['condition']['icon'],API_NAME='weatherAPI')
            city_weather.save() # Save result in DB.
      

class City(models.Model):

   '''Class for City model.  '''

   city_name = models.CharField(max_length=200)
   objects = CityManager()
class Weather(models.Model):

   '''Class for Weather model. '''
   
   temperature = models.FloatField()
   icon = models.CharField(max_length=4000)
   city_name = models.CharField(max_length=4000)
   API_NAME=models.CharField(max_length=4000)
   ERROR = models.TextField()
   date_of_getting = models.DateTimeField(auto_now=True)
      


