from django.test import TestCase
from .compressor import compress
from io import BytesIO
from PIL import Image
import sys

class EnhancerTest(TestCase):
    def test_compress_returns_smaller_image(self):
        # Read the image to take original image
        test_img_dir = "images/original.jpg"
        img = Image.open(test_img_dir)
        img_io = BytesIO()
        img.save(img_io, format = 'JPEG')
        ori_size = sys.getsizeof(img_io)

        # Compress the same image
        new_image = compress(test_img_dir)
        new_size = sys.getsizeof(new_image)

        self.assertTrue(ori_size > new_size)

    def test_compress_image_does_not_exist(self):
        test_img_dir = "images/original2.jpg"
        message = compress(test_img_dir)
        self.assertEquals(message, "The file images/original2.jpg does not exist.")
        