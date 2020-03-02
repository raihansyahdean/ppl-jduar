"""
Main module for tests in enhancer app.
"""
import base64
import sys
from io import BytesIO
from django.test import TestCase
from PIL import Image
from .compressor import compress
from .image_processor import delete_image, data_to_image, image_to_data

class EnhancerTest(TestCase):
    """
    Main enhancer test class.
    """
    def test_compress_returns_smaller_image(self):
        """
        Test to read an image from a directory and compare
        sizes after compression.
        """
        test_img_dir = "images/large.jpg"
        img = Image.open(test_img_dir)
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        ori_size = sys.getsizeof(img_io)

        compress(test_img_dir)
        new_image = Image.open("compressed_images/compressed_large.jpg")
        img_io2 = BytesIO()
        new_image.save(img_io2, format='JPEG')
        new_size = sys.getsizeof(img_io2)

        self.assertTrue(ori_size > new_size)

    def test_compress_image_does_not_exist(self):
        """
        Test when image does not exists return error message.
        """
        test_img_dir = "images/original2.jpg"
        message = compress(test_img_dir)
        self.assertEqual(message, "The file images/original2.jpg does not exist.")

    def test_convert_image_to_data_success(self):
        """
        Test to convert an image to base64.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        result = image_to_data(test_img_dir)

        image = Image.open(test_img_dir)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        self.assertEqual(result, base64.b64encode(buffered.getvalue()))

    def test_convert_image_to_data_file_not_found(self):
        """
        Test to convert an image fail when file not found.
        """
        test_img_dir = "compressed_images/compressed_large2.jpg"
        result = image_to_data(test_img_dir)
        self.assertEqual(result, "File compressed_images/compressed_large2.jpg not found.")

    def test_convert_data_to_image_success(self):
        """
        Test to convert a base64 data to an image.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        image = Image.open(test_img_dir)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        ret_msg = data_to_image(img_str, "decoded_image.jpg")
        self.assertEqual(ret_msg, "Successful convert to images/decoded_image.jpg")
        delete_image("images/decoded_image.jpg")

    def test_delete_image_successful(self):
        """
        Test to delete an image from a directory.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        message = delete_image(test_img_dir)
        self.assertEqual(message, "delete successful")

    def test_delete_image_does_not_exist(self):
        """
        Test when image does not exists return error message.
        """
        test_img_dir = "compressed_images/compressed_large2.jpg"
        message = delete_image(test_img_dir)
        self.assertEqual(message,
                         "The file compressed_images/compressed_large2.jpg does not exist.")
        