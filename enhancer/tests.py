"""
Main module for tests in enhancer app.
"""
import base64
import sys
from io import BytesIO
from django.test import TestCase
from PIL import Image
from .compressor import compress
from .image_processor import delete_image, data_to_image, image_to_data, create_register_payload

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
        with self.assertRaises(Exception) as the_error:
            compress(test_img_dir)
        err = the_error.exception
        self.assertEqual(str(err), "The file images/original2.jpg does not exist.")

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
        with self.assertRaises(Exception) as the_error:
            image_to_data(test_img_dir)
        err = the_error.exception
        self.assertEqual(str(err),
                         "File compressed_images/compressed_large2.jpg not found.")

    @staticmethod
    def test_convert_data_to_image_success():
        """
        Test to convert a base64 data to an image.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        image = Image.open(test_img_dir)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        data_to_image(img_str, "decoded_image.jpg")
        delete_image("images/decoded_image.jpg")

    @staticmethod
    def test_delete_image_successful():
        """
        Test to delete an image from a directory.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        delete_image(test_img_dir)

    def test_delete_image_does_not_exist(self):
        """
        Test when image does not exists return error message.
        """
        test_img_dir = "compressed_images/compressed_large2.jpg"
        with self.assertRaises(Exception) as the_error:
            delete_image(test_img_dir)
        err = the_error.exception
        self.assertEqual(str(err),
                         "The file compressed_images/compressed_large2.jpg does not exist.")

    def test_create_payload_correctly(self):
        """
        Test when payload will be created correctly.
        """
        test_img_dir = "images/large.jpg"
        data_str = image_to_data(test_img_dir)

        datas = []
        for _ in range(5):
            datas.append(data_str)
        payload = create_register_payload(datas)

        for i in range(5):
            cur_data = payload["data"][i]["image"]
            self.assertNotEqual(cur_data, "")

    def test_create_payload_datas_length_incorrect(self):
        """
        Test when payload have different lengths.
        """
        test_img_dir = "images/large.jpg"
        data_str = image_to_data(test_img_dir)

        datas = []
        for _ in range(4):
            datas.append(data_str)

        with self.assertRaises(Exception) as the_error:
            create_register_payload(datas)
        err = the_error.exception
        self.assertEqual(str(err), "Data length must be 5.")
