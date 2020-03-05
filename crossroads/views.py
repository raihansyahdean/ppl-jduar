"""
Crossroads views : communicate backend with frontend and dummy
"""
import json
import requests
from django.http import JsonResponse
import django.middleware.csrf
from django.views.decorators.csrf import csrf_exempt

import crossroads.validator as validator
import enhancer.image_processor as processor

INVALID_PAYLOAD_RESPONSE = {"status_code": 400, "message": "Invalid Payload"}
INVALID_REQUEST_RESPONSE = {"status_code": 400, "message": "Invalid Request"}


@csrf_exempt
def receive_photos_from_fe(request):
    """
    Receive photos from fe after registration
    :param request:
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        request_payload = json.loads(body_unicode)

        images = []
        for i in request_payload['images']:
            images.append(i[23:])

        ready_payload = processor.create_register_payload(images)
        print(ready_payload)
        response_api = send_photos_to_dummy(request, ready_payload)
        print(response_api)
        return response_api

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)


def send_photos_to_dummy(request, request_payload):
    """
    Send payload from backend to dummy
    For further use of customer registration to XQ Informatics API
    """
    
    if not validator.payload_isvalid(request_payload):
        print('fail')
        return JsonResponse(json.loads(json.dumps(INVALID_PAYLOAD_RESPONSE)), status=400)

    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('https://dummy-smartcrm.herokuapp.com/payload/photos/',
                             data=json.dumps(request_payload),
                             headers={"CSRF-Token": csrf_token})

    # Reformat response to appropriate json
    reformatted_response = response.content.decode('utf8').replace("\\", "")
    reformatted_response = reformatted_response[1:-1]  # Remove unnecessary '
    print('success')
    return JsonResponse(json.loads(reformatted_response))
