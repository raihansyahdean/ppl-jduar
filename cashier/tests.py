"""
Main module for tests in cashier app.
"""
import json
from django.test import TestCase, Client
import cashier.views as view


REGIST_PAYLOAD = json.dumps({
    "cashier_name":"real admin",
	"username": "admin",
	"cashier_password": "admin123",
	"merchant": "indojuni",
	"merchant_branch": "FMIPA"
})

LOGIN_PAYLOAD = json.dumps({
	"username": "admin",
	"cashier_password": "admin123"
})

class CashierTest(TestCase):
    """
    run test for crossroads app
    """
    def test_valid_regist_payload(self):
        """
        Test when payload sent is valid.
        """
        response = Client().post('/cashier/regist/', REGIST_PAYLOAD, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["auth"])

    def test_bad_regist_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/cashier/regist/")
        self.assertEqual(response.status_code, 400)

    def test_valid_login_payload(self):
        """
        Test when payload sent is valid.
        """
        response = Client().post('/cashier/login/', LOGIN_PAYLOAD, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["auth"])

    def test_bad_login_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/cashier/login/")
        self.assertEqual(response.status_code, 400)

    