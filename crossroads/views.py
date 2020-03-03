"""
Crossroads views : communicate backend with frontend and dummy
"""
import json
from django.http import JsonResponse
import django.middleware.csrf
import requests

IMAGE_TEMPLATE = "<image>"

PAYLOAD_TEMPLATE = {
    "data": [
        {
            "position": "front",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "right",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "left",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "bottom",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "top",
            "image": IMAGE_TEMPLATE
        }
    ]
}

INVALID_PAYLOAD_RESPONSE = {"status_code": 400, "message": "Invalid Payload"}


def send_photos_to_dummy(request):
    """
    Send payload from backend to dummy
    For further use of customer registration to XQ Informatics API
    """
    body_unicode = request.body.decode('utf8')
    request_payload = json.loads(body_unicode)
    if not payload_isvalid(request_payload):
        return JsonResponse(json.loads(json.dumps(INVALID_PAYLOAD_RESPONSE)), status=400)

    csrf_token = django.middleware.csrf.get_token(request)
    response = requests.post('http://dummy-smartcrm.herokuapp.com/payload/photos/',
                             data=json.dumps(request_payload),
                             headers={"CSRF-Token": csrf_token})

    # Reformat response to appropriate json
    reformatted_response = response.content.decode('utf8').replace("\\", "")
    reformatted_response = reformatted_response[1:-1]  # Remove unnecessary '
    return JsonResponse(json.loads(reformatted_response))


def payload_isvalid(payload):
    """
    Validate payload based on template.
    :param payload: dictionary that will be dumped to json and sent as payload
    :return: True if valid. False otherwise
    """
    valid_position_flag = {
        "front": False,
        "right": False,
        "left": False,
        "bottom": False,
        "top": False}
    try:
        data = payload["data"]

        # Check json keys
        for photos in data:
            position = photos["position"]
            # Check for duplicate direction
            if valid_position_flag[position]:
                print("invalid flag")
                return False
            valid_position_flag[position] = True
            image = photos["image"]
            if not isinstance(image, str):
                print("invalid type")
                return False

        # Check if there's missing images
        for value in valid_position_flag.values():
            if not value:
                print("Missing direction")
                return False

        return True

    except KeyError:
        return False
