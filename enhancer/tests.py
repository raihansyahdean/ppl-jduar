from django.test import TestCase
from .compressor import *
from io import BytesIO
from PIL import Image
import sys

test_img_dir = "images/original.jpg"

class EnhancerTest(TestCase):
    def test_compress_returns_smaller_image(self):
        # Read the image to take original
        img = Image.open(test_img_dir)
        img_io = BytesIO()
        img.save(img_io, format = 'JPEG')
        ori_size = sys.getsizeof(img_io)

        # Compress the same image
        new_image = compress(test_img_dir)
        print(new_image)
        