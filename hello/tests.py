from django.test import TestCase, Client

# Create your tests here.
def test_hello_world(self):
    response = Client().get("/hello/")
    self.assertEqual(response.status_code,200)
    self.assertEqual(response.message,"Hello World!")
