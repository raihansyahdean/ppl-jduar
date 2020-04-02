from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = 'crossroads'
urlpatterns = [
    path('regist/', receive_regist_photos, name='receive_regist_photos')
]
