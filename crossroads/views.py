from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_protect
import django.middleware.csrf
import requests
import json

def send_photos_to_dummy(request):
  return