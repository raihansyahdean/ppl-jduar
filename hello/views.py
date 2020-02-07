from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def hello_world(request):
    response = {
        "status_code": 200,
        "message" : "Hello World!"
    }
    return JsonResponse(response)