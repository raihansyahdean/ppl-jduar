from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = 'crossroads'
urlpatterns = [
	path('send/', send_photos_to_dummy,name='send_photos_to_dummy'),
]
