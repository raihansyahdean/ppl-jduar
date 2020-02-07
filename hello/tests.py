import json
from django.test import TestCase, Client

hello_body = {
    "status_code": 200,
    "message": "Hello World!"
}

# Create your tests here.
class HelloTest(TestCase):
    def test_hello_world(self):
        response = Client().get("/hello/")
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(str(response.content, encoding="utf8"),hello_body)