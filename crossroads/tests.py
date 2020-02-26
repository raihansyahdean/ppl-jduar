import json
from django.test import TestCase, Client

payload = {
    "registerPhoto":[
    {
      "position" : "front",
      "image" : "<image>"
    },
    {
      "position" : "right",
      "image" : "<image>"
    },
    {
      "position" : "left",
      "image" : "<image>"
    },
    {
      "position" : "bottom",
      "image" : "<image>"
    },
    {
      "position" : "top",
      "image" : "<image>"
    }
  ]
}

# Create your tests here.
class CrossroadTest(TestCase):
    def test_hello_world(self):
        response = Client().post("")
        self.assertEqual(response.status_code,200)