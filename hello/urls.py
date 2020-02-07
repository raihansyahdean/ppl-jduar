from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = 'hello'
urlpatterns = [
	path('', hello_world,name='hello_world'),
]
