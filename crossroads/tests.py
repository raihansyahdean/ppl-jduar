import json
from django.test import TestCase, Client

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
    def test_valid_payload(self):
        response = Client().post("/crossroads/send/", PAYLOAD, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_invalid_payload(self):
        response = Client().post("/crossroads/send/", INVALID_PAYLOAD, content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    def test_invalid_type_payload(self):
        response = Client().post("/crossroads/send/", INVALID_TYPE_PAYLOAD, content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    def test_invalid_key_payload(self):
        response = Client().post("/crossroads/send/", INVALID_KEY_PAYLOAD, content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")

    def test_incomplete_payload(self):
        response = Client().post("/crossroads/send/", INCOMPLETE_PAYLOAD, content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Payload")
