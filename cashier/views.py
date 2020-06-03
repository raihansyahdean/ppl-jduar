import json
import jwt
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cashier.models import Cashier

INVALID_REQUEST_RESPONSE = {"status_code": 400, "message": "Invalid Request"}
DUPLICATE_USERNAME_RESPONSE = {"status_code": 500, "message": "Duplicate Username Error"}
DATABASE_ERROR_RESPONSE = {"status_code": 500, "message": "Database Error"}
WRONG_PASSWORD_RESPONSE = {"status_code": 403, "message": "Wrong Password"}


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

        # TODO Validasi data diatas berdasarkan database dab Masukin kedalam database
        new_cashier = Cashier(cashier_name=cashier_name,
                              username=username,
                              cashier_password=cashier_password,
                              merchant=merchant,
                              merchant_branch=merchant_branch)

        if Cashier.objects.filter(username=username).exists():
            return JsonResponse(json.loads(json.dumps(DUPLICATE_USERNAME_RESPONSE)), status=500)

        try:
            new_cashier.save()
        except:
            return JsonResponse(json.loads(json.dumps(DATABASE_ERROR_RESPONSE)), status=500)

        token = jwt.encode({'user': username}, 'SECRET', algorithm='HS256')
        payload = {"auth": True, "token": token.decode(), "user": username}
        response = json.dumps(payload)

        return JsonResponse(json.loads(response), status=200)

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

        # TODO Validasi data diatas berdasarkan database
        cashier = Cashier.objects.get(username=username)
        if cashier is None or cashier_password != cashier.cashier_password:
            return JsonResponse(json.loads(json.dumps(WRONG_PASSWORD_RESPONSE)), status=403)

        token = jwt.encode({'user': username}, 'SECRET', algorithm='HS256')
        payload = {"auth": True, "token": token.decode(), "user": username}
        response = json.dumps(payload)

        return JsonResponse(json.loads(response), status=200)

    return JsonResponse(json.loads(json.dumps(INVALID_REQUEST_RESPONSE)), status=400)
