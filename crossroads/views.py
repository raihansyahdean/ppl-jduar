from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_protect
import django.middleware.csrf
import requests
import json

payload_example = {
    "registerPhoto": [
        {
            "position": "front",
            "image": "<image>"
        },
        {
            "position": "right",
            "image": "<image>"
        },
        {
            "position": "left",
            "image": "<image>"
        },
        {
            "position": "bottom",
            "image": "<image>"
        },
        {
            "position": "top",
            "image": "<image>"
        }
    ]
}


def send_photos_to_dummy(request):
    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('http://dummy-smartcrm.herokuapp.com/payload/photos/', data=json.dumps(payload_example),
                             headers={"CSRF-Token": csrf_token})
    print(response)
    return HttpResponse(response)
