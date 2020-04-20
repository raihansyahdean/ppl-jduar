from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = 'crossroads'
urlpatterns = [
    path('regist/', receive_regist_photos, name='receive_regist_photos'),
    path('identify/', receive_identification_photo, name='receive_identification_photo'),
    path('registpasscode/', receive_regist_passcode, name='receive_regist_passcode'),
    path('identifypasscode/', receive_identification_passcode, name='receive_identification_passcode')
]
