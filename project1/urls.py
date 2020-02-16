"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from weather import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view


router = DefaultRouter()
router.register('api/v1/city',views.CityAPIView,basename='City')
router.register('api/v1/weather',views.WeatherAPIView,basename='Weather')
schema_view = get_swagger_view(title='REST API for simple weather project',patterns=router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.WeatherLoginView.as_view(),name='login_url'),
    path('logout',auth_views.LogoutView.as_view(),name='logout_url'),
    path('signup/',views.CustomUserCreate.as_view(),name='signup_url'),
    path('profile/<int:pk>/',views.CustomUserUpdate.as_view(),name='profile_url'),
    path('',views.IndexView.as_view(),name='index_url'),
    path('api/v1/',schema_view,name='api_url'),

]
#urlpatterns += router.urls


