from rest_framework import serializers
from .models import City, Weather
class CitySerializer(serializers.ModelSerializer):

    '''Simple serializer for City model objects. '''

    class Meta:

        model = City
        fields = ('city_name',)

class WeatherSerializer(serializers.ModelSerializer):

    '''Simple serializer for Weather model objects. '''

    class Meta:

        model = Weather
        fields  = ('city_name','temperature','API_NAME','date_of_getting',)
