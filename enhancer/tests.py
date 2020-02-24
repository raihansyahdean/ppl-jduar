from django.test import TestCase
from .compressor import *

# Create your tests here.
class EnhancerTest(TestCase):
    def test_compressor(self):
        new_image = compress("original.jpg")
        print(new_image)