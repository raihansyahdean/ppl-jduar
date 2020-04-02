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

# Response Templates
INVALID_REQUEST_RESPONSE = {"status_code": 400, "message": "Invalid Request"}
CREATE_REGIST_PAYLOAD_FAILED_RESPONSE = {
    "status_code": 500,
    "message": "Internal Server: Create Register Payload Failed"
}
INVALID_REGIST_PAYLOAD_RESPONSE = {
    "status_code": 500,
    "message": "Internal Server: Invalid Register Payload"
}

@csrf_exempt
def receive_regist_photos(request):
    """
    Receive photos from fe after registration
    :param request:
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        regist_payload = json.loads(body_unicode)

        images = []
        for i in regist_payload['images']:
            images.append(i[23:])
        try:
            ready_payload = processor.create_register_payload(images)
        except:
            return JsonResponse(json.loads(
                json.dumps(CREATE_REGIST_PAYLOAD_FAILED_RESPONSE)), status=500)

        response_api = send_regist_photos(request, ready_payload)
        return response_api

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)

def send_regist_photos(request, request_payload):
    """
    Send payload from backend to dummy
    For further use of customer registration to XQ Informatics API
    """
    try:
        validator.validate_regist_payload(request_payload)
    except:
        return JsonResponse(json.loads(json.dumps(INVALID_REGIST_PAYLOAD_RESPONSE)), status=500)

    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('https://dummy-smartcrm.herokuapp.com/payload/photos/',
                             data=json.dumps(request_payload),
                             headers={"CSRF-Token": csrf_token})

    # Reformat response to appropriate json
    reformatted_response = response.content.decode('utf8').replace("\\", "")
    reformatted_response = reformatted_response[1:-1]
    return JsonResponse(json.loads(reformatted_response))
