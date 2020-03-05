from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = 'crossroads'
urlpatterns = [
    path('regist/', receive_photos_from_fe, name='receive_photos_from_fe')
]
