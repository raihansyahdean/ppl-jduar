from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = 'cashier'
urlpatterns = [
    path('regist/', receive_regist_data, name='receive_regist_data'),
    path('login/', receive_login_data, name='receive_login_data')
]
