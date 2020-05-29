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
CREATE_REGIST_PAYLOAD_BAD_IMAGE = {
    "status_code": 500,
    "message": "Bad Regist Image Sent: To Blurry"
}
INVALID_REGIST_PAYLOAD_RESPONSE = {
    "status_code": 500,
    "message": "Internal Server: Invalid Register Payload"
}
INVALID_REGIST_PASSCODE_PAYLOAD = {
    "status_code": 400,
    "message": "Invalid Register Passcode Payload"
}

CREATE_IDENTIFICATION_PAYLOAD_FAILED_RESPONSE = {
    "status_code": 500,
    "message": "Internal Server: Create Identification Payload Failed"
}
CREATE_IDENTIFICATION_PAYLOAD_BAD_IMAGE = {
    "status_code": 500,
    "message": "Bad Identify Image Sent: To Blurry"
}
INVALID_IDENTIFICATION_PAYLOAD_RESPONSE = {
    "status_code": 500,
    "message": "Internal Server: Invalid Identification Payload"
}
INVALID_IDENTIFY_PAYLOAD_RESPONSE = {
    "status_code": 500,
    "message": "Internal Server: Invalid Identify Payload"
}
INVALID_IDENTIFY_PASSCODE_PAYLOAD = {
    "status_code": 400,
    "message": "Invalid Identify Passcode Payload"
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
        except Exception as exc:
            print("[REGIST_PHOTOS_RECEIVE] " + str(exc))
            if str(exc) == "Bad Image Sent":
                print("BAD_REGIST_IMAGE")
                return JsonResponse(json.loads(
                    json.dumps(CREATE_REGIST_PAYLOAD_FAILED_RESPONSE)), status=500)

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
    except Exception as exc:
        print("[REGIST_PHOTOS_SEND] " + str(exc))
        return JsonResponse(json.loads(json.dumps(INVALID_REGIST_PAYLOAD_RESPONSE)), status=500)

    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('https://dummy-smartcrm.herokuapp.com/payload/photos/',
                             data=json.dumps(request_payload),
                             headers={"CSRF-Token": csrf_token})

    # Reformat response to appropriate json
    reformatted_response = response.content.decode('utf8').replace("\\", "")
    reformatted_response = reformatted_response[1:-1]
    return JsonResponse(json.loads(reformatted_response))

@csrf_exempt
def receive_identification_photo(request):
    """
    Receive photos from fe after registration
    :param request:
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        regist_payload = json.loads(body_unicode)

        image = regist_payload['image'][23:]
        try:
            ready_payload = processor.create_identification_payload(image)
        except Exception as exc:
            print("[IDENT_PHOTOS_RECEIVE] " + str(exc))
            if str(exc) == "Bad Image Sent":
                print("BAD_IDENTIFICATION_IMAGE")
                return JsonResponse(json.loads(
                    json.dumps(CREATE_IDENTIFICATION_PAYLOAD_BAD_IMAGE)), status=500)

            return JsonResponse(json.loads(
                json.dumps(CREATE_IDENTIFICATION_PAYLOAD_FAILED_RESPONSE)), status=500)

        response_api = send_identification_photo(request, ready_payload)
        return response_api

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)

def send_identification_photo(request, request_payload):
    """
    Send payload from backend to dummy
    For further use of customer registration to XQ Informatics API
    """
    try:
        validator.validate_identification_payload(request_payload)
    except Exception as exc:
        print("[IDENT_PHOTOS_SEND] " + str(exc))
        return JsonResponse(json.loads(json.dumps(INVALID_IDENTIFICATION_PAYLOAD_RESPONSE)), status=500)

    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('https://dummy-smartcrm.herokuapp.com/payload/identify-photos/',
                             data=json.dumps(request_payload),
                             headers={"CSRF-Token": csrf_token})

    # Reformat response to appropriate json
    reformatted_response = response.content.decode('utf8').replace("\\", "")
    reformatted_response = reformatted_response[1:-1]
    return JsonResponse(json.loads(reformatted_response))

@csrf_exempt
def receive_regist_passcode(request):
    """
    Handle request from FE for passcode registration
    :param request: chosen passcode in json
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        regist_passcode_payload = json.loads(body_unicode)

        try:
            validator.validate_regist_passcode_payload(regist_passcode_payload)
        except Exception as exc:
            print("[REGIST_PASS_RECEIVE] " + str(exc))
            return JsonResponse(json.loads(json.dumps(INVALID_REGIST_PASSCODE_PAYLOAD)), status=400)

        csrf_token = django.middleware.csrf.get_token(request)
        response = requests.post('https://dummy-smartcrm.herokuapp.com/payload/password/',
                                 data=json.dumps(regist_passcode_payload),
                                 headers={"CSRF-Token": csrf_token})

        # Reformat response to appropriate json
        reformatted_response = response.content.decode('utf8').replace("\\", "")
        reformatted_response = reformatted_response[1:-1]
        return JsonResponse(json.loads(reformatted_response))

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)

@csrf_exempt
def receive_identification_passcode(request):
    """
    Handle request from FE for passcode identification
    :param request: passcode in json
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        identify_passcode_payload = json.loads(body_unicode)

        try:
            validator.validate_identification_passcode_payload(identify_passcode_payload)
        except Exception as exc:
            print("[IDENT_PASS_RECEIVE] " + str(exc))
            return JsonResponse(json.loads(json.dumps(INVALID_IDENTIFY_PASSCODE_PAYLOAD)), status=400)

        csrf_token = django.middleware.csrf.get_token(request)
        response = requests.post('https://dummy-smartcrm.herokuapp.com/payload/identify-passcode/',
                                 data=json.dumps(identify_passcode_payload),
                                 headers={"CSRF-Token": csrf_token})

        # Reformat response to appropriate json
        reformatted_response = response.content.decode('utf8').replace("\\", "")
        reformatted_response = reformatted_response[1:-1]
        return JsonResponse(json.loads(reformatted_response))

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)
