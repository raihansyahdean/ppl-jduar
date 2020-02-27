import json
from django.shortcuts import HttpResponse
import django.middleware.csrf
import requests

PAYLOAD_EXAMPLE = {
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
    """
    Send payload from backend to dummy
    For further use of customer registration to XQ Informatics API
    """
    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('http://dummy-smartcrm.herokuapp.com/payload/photos/',
                             data=json.dumps(PAYLOAD_EXAMPLE),
                             headers={"CSRF-Token": csrf_token})
    print(response)
    return HttpResponse(response)
