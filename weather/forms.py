from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import requests
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):

        model=CustomUser
        fields=('username','email')

class CustomUserChangeForm(UserChangeForm):

    '''Form for change customuser fields. '''
    def clean(self):

        '''Function checks than one of three checkboxes selected.'''

        open_weather_map=self.cleaned_data['open_weather_map'] # Get value from cleaned_data.
        weather_api = self.cleaned_data['weather_api'] # Get value from cleaned_data.
        world_weather_online = self.cleaned_data['world_weather_online'] # Get value from cleaned_data.
        if not open_weather_map and not weather_api and not world_weather_online: # If all three == False then raise Error
            raise forms.ValidationError('One of API must be selected',code=12)
        return super().clean() # Else call super method.

    class Meta(UserChangeForm):

        model = CustomUser
        favorite_cities = forms.CharField(max_length=4000,required = False,label='Please enter citites where  you need check weather everyday',widget=forms.TextInput(attrs={'placeholder': 'Please enter city or cities through ",". For example:London,Paris,etc.', 'size':'70'}))
        open_weather_map = forms.CheckboxInput()
        weather_api = forms.CheckboxInput()
        username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'disabled':'True'}))
        world_weather_online=forms.CheckboxInput()
        fields = ('username','email','favorite_cities','open_weather_map','weather_api','world_weather_online')
        
        
                 
class IndexForm(forms.Form): 

    '''Class for IndexForm '''
    city_name=forms.CharField(max_length=4000,label='Enter city',widget=forms.TextInput(attrs={'placeholder': 'Please enter city or cities through ",". For example:London,Paris,etc.', 'size':'52'}))
    def get_weather_open_weather_map(self):

        '''Function for getting weather for city/cities if it added in IndexForm. '''

        open_weather_map_api_key = '68b12f971d6b5bb4fbf4c5239217920e' #api_key, mb better save it in db
        weather_api_key = '09d4b44352f946a0ba6142526200801'
        world_weather_online_api_key = 'a48fa20f6ca14616865142928200801'
        if self.cleaned_data['city_name'] is None or len(self.cleaned_data['city_name'])>4000: # Check then field not None and less then 4000 .
            raise ValidationError 
        url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+open_weather_map_api_key #Get correct Url to API.
        all_cities=[]
        cities=self.cleaned_data['city_name'].split(",") # Get list from string.
        for i in cities:
            res=requests.get(url.format(i)).json() #Get response from API.
            if res.get('message')=='city not found': # Check what city is real.
                city_info={
                    'city':i,
                    'message':res.get('message')
                }
                all_cities.append(city_info)
                continue
            city_info={
                'city':i, #Get city_name.
                'temp':res["main"]["temp"], #Get temp.
                'icon':res["weather"][0]["icon"] #Get icon.
            }
            all_cities.append(city_info)
        return all_cities    # Return cities list with data.
class AuthUserForm(AuthenticationForm,forms.ModelForm):

    '''Class for auth users. '''
    
    class Meta:
        model=CustomUser
        username = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'size':'5'}))
        password=forms.CharField(max_length=254,widget=forms.PasswordInput(attrs={'size':'5'}))
        fields = ('username','password')