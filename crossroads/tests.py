"""
Main module for tests in crossroads app.
"""
import json
from django.test import TestCase, Client
from django.test.client import RequestFactory
import crossroads.views as view
import enhancer.image_processor as processor

INVALID_REGIST_PAYLOAD_FROM_FE = {
    "images": [
        "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
        "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
        "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
        "this is dummy image, this is dummy image, this is dummy image, this is dummy image",
        "this is dummy image, this is dummy image, this is dummy image, this is dummy image"
    ]
}

VALID_REGIST_PAYLOAD_FROM_FE = {
    "images": []
}

REGIST_PAYLOAD = {
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

INCOMPLETE_REGIST_PAYLOAD = {
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

DUPLICATE_POS_REGIST_PAYLOAD = {
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

INVALID_IMAGE_TYPE_REGIST_PAYLOAD = {
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

INVALID_POS_REGIST_PAYLOAD = {
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

VALID_REGIST_PASSCODE_PAYLOAD = {
    "chosen_passcode": "Grapes"
}

INVALID_FRUIT_TYPE_REGIST_PASSCODE_PAYLOAD = {
    "chosen_passcode": "Sushi"
}

INVALID_KEY_REGIST_PASSCODE_PAYLOAD = {
    "passcode": "Grapes"
}

VALID_IDENTIFICATION_PAYLOAD = {
    "image": "<image>"
}

INVALID_KEY_IDENTIFICATION_PAYLOAD = {
    "myimage": "<image>"
}

INVALID_IMAGE_TYPE_IDENTIFICATION_PAYLOAD = {
    "image": 333333
}

INVALID_IMAGE_EMPTY_IDENTIFICATION_PAYLOAD = {
    "image": ""
}

INVALID_IDENTIFICATION_PAYLOAD_FROM_FE = {
    "image": "this is dummy image, this is dummy image, this is dummy image, this is dummy image"
}

VALID_IDENTIFICATION_PAYLOAD_FROM_FE = {
    "image": ""
}

VALID_IDENTIFICATION_PASSCODE_PAYLOAD = {
    "passcode": "Grapes"
}

FAIL_IDENTIFICATION_PASSCODE_PAYLOAD = {
    "passcode": "Watermelon"
}

INVALID_FRUIT_TYPE_IDENTIFICATION_PASSCODE_PAYLOAD = {
    "passcode": "Sushi"
}

INVALID_KEY_IDENTIFICATION_PASSCODE_PAYLOAD = {
    "password": "Grapes"
}


class CrossroadTest(TestCase):
    """
    run test for crossroads app
    """

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @staticmethod
    def set_valid_regist_payload_from_fe():
        """
        Function to set up the valid regist payload
        from FE: array of 5 images in bytes.
        """
        test_img_dir = "images/original.jpg"
        img_str = processor.image_to_data(test_img_dir)
        img_str = img_str.decode("utf-8")
        img_str = "zzzzzzzzzzyyyyyyyyyyxxx" + img_str
        for _ in range(5):
            VALID_REGIST_PAYLOAD_FROM_FE["images"].append(img_str)

    @staticmethod
    def set_valid_identification_payload_from_fe():
        """
        Function to set up the valid identification payload
        from FE: 1 image in bytes.
        """
        test_img_dir = "images/original.jpg"
        img_str = processor.image_to_data(test_img_dir)
        img_str = img_str.decode("utf-8")
        img_str = "zzzzzzzzzzyyyyyyyyyyxxx" + img_str
        VALID_IDENTIFICATION_PAYLOAD_FROM_FE["image"] = img_str

    # Register Validation Tests to XQ (dummy)
    def test_valid_regist_payload(self):
        """
        Test when payload sent is valid.
        """
        request = self.factory.get('/crossroads/regist/', REGIST_PAYLOAD)

        response = view.send_regist_photos(request, REGIST_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["available_passcodes"])

    def test_duplicate_pos_regist_payload(self):
        """
        Test when payload is invalid.
        """
        request = self.factory.get('/crossroads/regist/', DUPLICATE_POS_REGIST_PAYLOAD)

        response = view.send_regist_photos(request, DUPLICATE_POS_REGIST_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"], "Internal Server: Invalid Register Payload")

    def test_invalid_image_type_regist_payload(self):
        """
        Test when payload type is invalid.
        """
        request = self.factory.get('/crossroads/regist/', INVALID_IMAGE_TYPE_REGIST_PAYLOAD)

        response = view.send_regist_photos(request, INVALID_IMAGE_TYPE_REGIST_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"], "Internal Server: Invalid Register Payload")

    def test_invalid_pos_regist_payload(self):
        """
        Test when payload key is invalid.
        """
        request = self.factory.get('/crossroads/regist/', INVALID_POS_REGIST_PAYLOAD)

        response = view.send_regist_photos(request, INVALID_POS_REGIST_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"], "Internal Server: Invalid Register Payload")

    def test_incomplete_regist_payload(self):
        """
        Test when payload is incomplete.
        """
        request = self.factory.get('/crossroads/regist/', INCOMPLETE_REGIST_PAYLOAD)

        response = view.send_regist_photos(request, INCOMPLETE_REGIST_PAYLOAD)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"], "Internal Server: Invalid Register Payload")

    # Test Receive Requests from FE
    def test_bad_regist_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/crossroads/regist/")
        self.assertEqual(response.status_code, 400)

    def test_invalid_regist_payload_from_fe(self):
        """
        Test when receive invalid payload post from frontend.
        """
        response = Client().post("/crossroads/regist/", \
                                 INVALID_REGIST_PAYLOAD_FROM_FE, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_valid_regist_payload_from_fe(self):
        """
        Test when receive valid payload post from frontend.
        """
        self.set_valid_regist_payload_from_fe()

        response = Client().post('/crossroads/regist/', \
                                 data=json.dumps(VALID_REGIST_PAYLOAD_FROM_FE), \
                                 content_type="application/json")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["available_passcodes"])

    # Test Receive Passcode From FE
    def test_bad_regist_passcode_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/crossroads/registpasscode/")
        self.assertEqual(response.status_code, 400)

    def test_invalid_key_regist_passcode_payload_from_fe(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        response = Client().post("/crossroads/registpasscode/",
                                 INVALID_KEY_REGIST_PASSCODE_PAYLOAD, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_fruit_type_regist_passcode_payload_from_fe(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        response = Client().post("/crossroads/registpasscode/",
                                 INVALID_FRUIT_TYPE_REGIST_PASSCODE_PAYLOAD, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_regist_passcode_payload_from_fe(self):
        """
        Test when receive valid payload post from frontend.
        """
        response = Client().post('/crossroads/registpasscode/',
                                 data=json.dumps(VALID_REGIST_PASSCODE_PAYLOAD),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)

    # Identification Validation Tests to XQ (dummy)
    def test_valid_identification_payload(self):
        """
        Test when payload sent is valid.
        """
        request = self.factory.get('/crossroads/identify/', VALID_IDENTIFICATION_PAYLOAD)

        response = view.send_identification_photo(request, VALID_IDENTIFICATION_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["passcode_set"])

    def test_invalid_key_identification_payload(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        request = self.factory.get('/crossroads/identify/', INVALID_KEY_IDENTIFICATION_PAYLOAD)

        response = view.send_identification_photo(request, INVALID_KEY_IDENTIFICATION_PAYLOAD)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertEqual(data["message"], "Internal Server: Invalid Identification Payload")

    def test_invalid_image_type_identification_payload(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        request = self.factory.get('/crossroads/identify/', INVALID_IMAGE_TYPE_IDENTIFICATION_PAYLOAD)

        response = view.send_identification_photo(request, INVALID_IMAGE_TYPE_IDENTIFICATION_PAYLOAD)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertEqual(data["message"], "Internal Server: Invalid Identification Payload")

    def test_invalid_image_empty_identification_payload(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        request = self.factory.get('/crossroads/identify/', INVALID_IMAGE_EMPTY_IDENTIFICATION_PAYLOAD)

        response = view.send_identification_photo(request, INVALID_IMAGE_EMPTY_IDENTIFICATION_PAYLOAD)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertEqual(data["message"], "Internal Server: Invalid Identification Payload")

    # Test Receive identification Requests from FE
    def test_bad_identification_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/crossroads/identify/")
        self.assertEqual(response.status_code, 400)

    def test_invalid_identification_payload_from_fe(self):
        """
        Test when receive invalid payload post from frontend.
        """
        response = Client().post("/crossroads/identify/", \
                                 INVALID_IDENTIFICATION_PAYLOAD_FROM_FE, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_valid_identification_payload_from_fe(self):
        """
        Test when receive valid payload post from frontend.
        """
        self.set_valid_identification_payload_from_fe()

        response = Client().post('/crossroads/identify/', \
                                 data=json.dumps(VALID_IDENTIFICATION_PAYLOAD_FROM_FE), \
                                 content_type="application/json")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["passcode_set"])

    # Test Receive Identification Passcode From FE
    def test_bad_identification_passcode_request_from_fe(self):
        """
        Test invalid request.
        """
        response = Client().get("/crossroads/identifypasscode/")
        self.assertEqual(response.status_code, 400)

    def test_invalid_key_identification_passcode_payload_from_fe(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        response = Client().post("/crossroads/identifypasscode/",
                                 INVALID_KEY_IDENTIFICATION_PASSCODE_PAYLOAD, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_fruit_type_identification_passcode_payload_from_fe(self):
        """
        Test when receive invalid key in payload post from frontend.
        """
        response = Client().post("/crossroads/identifypasscode/",
                                 INVALID_FRUIT_TYPE_IDENTIFICATION_PASSCODE_PAYLOAD, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_identification_passcode_payload_from_fe(self):
        """
        Test when receive valid payload post from frontend.
        """
        response = Client().post('/crossroads/identifypasscode/',
                                 data=json.dumps(VALID_IDENTIFICATION_PASSCODE_PAYLOAD),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["message"], "User Identification Successful")

    def test_fail_identification_passcode_payload_from_fe(self):
        """
        Test when receive valid payload post from frontend.
        """
        response = Client().post('/crossroads/identifypasscode/',
                                 data=json.dumps(FAIL_IDENTIFICATION_PASSCODE_PAYLOAD),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["message"], "User Identification Failed: Passcode Incorrect")
