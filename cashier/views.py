import json
import jwt
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

INVALID_REQUEST_RESPONSE = {"status_code": 400, "message": "Invalid Request"}

@csrf_exempt
def receive_regist_data(request):
    """
    Receive data from fe after cashier registration
    :param request:
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        regist_payload = json.loads(body_unicode)

        cashier_name = regist_payload['cashier_name']
        username = regist_payload['username']
        cashier_password = regist_payload['cashier_password']
        merchant = regist_payload['merchant']
        merchant_branch = regist_payload['merchant_branch']

        #TODO Validasi data diatas berdasarkan database dab Masukin kedalam database

        token = jwt.encode({'user': username}, 'SECRET', algorithm='HS256')
        payload = { "auth": True, "token": token.decode(), "user": username }
        response = json.dumps(payload)

        return JsonResponse(json.loads(response))

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)

@csrf_exempt
def receive_login_data(request):
    """
    Receive data from fe after cashier login
    :param request:
    :return:
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf8')
        regist_payload = json.loads(body_unicode)

        username = regist_payload['username']
        cashier_password = regist_payload['cashier_password']

        #TODO Validasi data diatas berdasarkan database

        token = jwt.encode({'user': username}, 'SECRET', algorithm='HS256')
        payload = { "auth": True, "token": token.decode(), "user": username }
        response = json.dumps(payload)

        return JsonResponse(json.loads(response))

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)