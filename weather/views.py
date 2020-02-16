import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.views import LoginView
from .forms import IndexForm,AuthUserForm,CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Weather,City
from rest_framework import viewsets
from .serializers import CitySerializer,WeatherSerializer
# Create your views here.
class WeatherLoginView(LoginView):

    ''' View for User Login. '''

    template_name='login.html'
    authentication_form=AuthUserForm
    next = 'project1:profile_url'
    

    
class CustomUserCreate(CreateView):

    ''' View for User registration '''

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "weather/signup.html"
    def get_success_url(self):
        return '/'

class CustomUserUpdate(UpdateView):

    '''View for update user settings. '''

    model = CustomUser
    template_name = 'weather/profile.html'
    form_class = CustomUserChangeForm
    def get_object(self,queryset=None):
        return CustomUser.objects.get(pk=self.kwargs['pk'])

class IndexView(View): 

    ''' View for drawing index page of site. '''

    def get(self,request):

        '''Function for http GET method. '''

        auth = request.user.is_authenticated 
        if auth : # If user authenticated.
            form = IndexForm()
            weather_api1,weather_api2,weather_api3 = CustomUser.objects.get_weather_favorite_cities_auth_users(request.user.pk) # get weather from personal user list.
            context = {'weather_api1':weather_api1,'weather_api2':weather_api2,'weather_api3':weather_api3,'form':form}
            return render(request,'weather/index.html',context) # Return data.
        else: # Else call get_weather_favorite_cities_notauth_users.
            form = IndexForm()
            all_cities=CustomUser.objects.get_weather_favorite_cities_notauth_users()
            context = {'weather_info':all_cities,'form':form}
            return render(request,'weather/index.html',context)

    def post(self,request):

        '''Function for http POST method. '''

        bound_form=IndexForm(request.POST) # Get form with data from request.
        all_cities=[]
        auth = request.user.is_authenticated
        cities=[]
        if bound_form.is_valid():
            if auth :
                weather_api1,weather_api2,weather_api3 = CustomUser.objects.get_weather_favorite_cities_auth_users(request.user.pk) # Get weather from DB for user list.
                cities = bound_form.get_weather_open_weather_map() # Get info from API for city in IndexForm.
                form = IndexForm()
                context = {'weather_api1':weather_api1,'weather_api2':weather_api2,'weather_api3':weather_api3,'form':form,'cities':cities}
            else:
                all_cities=CustomUser.objects.get_weather_favorite_cities_notauth_users() # Get weather from DB for CONST_SITIES.
                cities = bound_form.get_weather_open_weather_map() # Get info from API for city in IndexForm.
                form = IndexForm()
                context = {'weather_info':all_cities,'cities':cities,'form':form}
            return render (request, 'weather/index.html', context) # Return data.

class CityAPIView(viewsets.ModelViewSet):
    
    '''Simple class for CRUD-model city model object. '''
    
    serializer_class = CitySerializer
    queryset = City.objects.all()

class WeatherAPIView(viewsets.ModelViewSet):

    ''' Simple class for CRUD-model weather model object. '''

    serializer_class = WeatherSerializer
    queryset = Weather.objects.all()