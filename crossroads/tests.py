"""
Main module for tests in crossroads app.
"""
import json
from django.test import TestCase, Client
from django.test.client import RequestFactory
import crossroads.views as view

# PAYLOAD_FROM_FE = {
#     "images": [
#             "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
#             "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
#             "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
#             "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
#             "this is dummy image, this is dummy image, this is dummy image, this is dummy image"]
# }

PAYLOAD = {
    "data": [
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

INCOMPLETE_PAYLOAD = {
    "data": [
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
        }
    ]
}

INVALID_PAYLOAD = {
    "data": [
        {
            "position": "front",
            "image": "<image>"
        },
        {
            "position": "front",
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

INVALID_TYPE_PAYLOAD = {
    "data": [
        {
            "position": "front",
            "image": 123512
        },
        {
            "position": "right",
            "image": 132421
        },
        {
            "position": "left",
            "image": 215125
        },
        {
            "position": "bottom",
            "image": 71364
        },
        {
            "position": "top",
            "image": 346243
        }
    ]
}

INVALID_KEY_PAYLOAD = {
    "data": [
        {
            "position": "frofssdfgnt",
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


# Create your tests here.
class CrossroadTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    """
    Main crossroads test class.
    """
    def test_valid_payload_to_dummy(self):
        """
        Test when payload sent is valid.
        """
        request = self.factory.get('/crossroads/regist/', PAYLOAD)

        response = view.send_photos_to_dummy(request, PAYLOAD)
        self.assertEqual(response.status_code, 200)

    def test_invalid_payload_to_dummy(self):
        """
        Test when payload is invalid.
        """
        request = self.factory.get('/crossroads/regist/', INVALID_PAYLOAD)

        response = view.send_photos_to_dummy(request, INVALID_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    def test_invalid_type_payload_to_dummy(self):
        """
        Test when payload type is invalid.
        """
        request = self.factory.get('/crossroads/regist/', INVALID_TYPE_PAYLOAD)

        response = view.send_photos_to_dummy(request, INVALID_TYPE_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    def test_invalid_key_payload_to_dummy(self):
        """
        Test when payload key is invalid.
        """
        request = self.factory.get('/crossroads/regist/', INVALID_KEY_PAYLOAD)

        response = view.send_photos_to_dummy(request, INVALID_KEY_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    def test_incomplete_payload_to_dummy(self):
        """
        Test when payload is incomplete.
        """
        request = self.factory.get('/crossroads/regist/', INCOMPLETE_PAYLOAD)

        response = view.send_photos_to_dummy(request, INVALID_KEY_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    # def test_receive_from_fe(self):
    #     """
    #     Test when receive post from frontend.
    #     """
    #     response = Client().post("/crossroads/regist/", PAYLOAD_FROM_FE, content_type="application/json")
    #     self.assertEqual(response.status_code, 200)

    def test_invalid_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/crossroads/regist/")
        self.assertEqual(response.status_code, 400)
