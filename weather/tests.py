from django.test import TestCase
from django.test.client import Client
from weather.forms import IndexForm
from weather.models import City, Weather

# Create your tests here.
class TestResponseCode(TestCase):

    '''Simple tests for checking that response code is 200. '''

    def test_login_page(self):

        '''Simple test for checking that response code from login page is 200. '''

        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code,200)
        
    def test_signup_page(self):
        
        '''Simple test for checking that response code from signup page is 200. '''

        client = Client()
        response = client.get('/signup/')
        self.assertEqual(response.status_code,200)

    def test_api_page(self):

        '''Simple test for checking that response code from api page is 200. '''

        client = Client()
        response = client.get('/api/v1/')
        self.assertEqual(response.status_code,200)

class TestIndexForm(TestCase):

    ''' Simple class for testing IndexForm '''

    def test_digits_in_index_form(self):
         
        ''' Function for checking digits in IndexForm, if it is , than raise error from API. '''
        form_data = {'city_name':'3123123123132'}
        form = IndexForm(form_data)
        form.is_valid()
        result = form.get_weather_open_weather_map()
        self.assertIsNotNone(result[0].get('message'))

class TestCityModel(TestCase):
    
    ''' Simple class for testing city manager methods . '''

    def test_get_weather_from_openweatherapi(self):

        ''' Simple funcion for testing get_weather_from_openweather_api method of City model. ''' 
        
        city = City (city_name = 'Samara')
        city.save()
        City.objects.get_weather_from_openweatherapi()
        self.assertIsNotNone(Weather.objects.get(city_name='Samara'))


