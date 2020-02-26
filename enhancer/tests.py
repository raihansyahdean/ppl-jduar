"""
Main module for tests in enhancer app.
"""
import sys
from io import BytesIO
from django.test import TestCase
from PIL import Image
from .compressor import compress

class EnhancerTest(TestCase):
    """
    Main enhancer test class.
    """
    def test_compress_returns_smaller_image(self):
        """
        Test to read an image from a directory and compare
        sizes after compression.
        """
        test_img_dir = "images/original.jpg"
        img = Image.open(test_img_dir)
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        ori_size = sys.getsizeof(img_io)

        new_image = compress(test_img_dir)
        new_size = sys.getsizeof(new_image)

        self.assertTrue(ori_size > new_size)

    def test_compress_image_does_not_exist(self):
        """
        Test when image does not exists return error message.
        """
        test_img_dir = "images/original2.jpg"
        message = compress(test_img_dir)
        self.assertEqual(message, "The file images/original2.jpg does not exist.")
        