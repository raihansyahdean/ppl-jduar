"""
Main module for tests in enhancer app.
"""
import base64
import sys
from io import BytesIO
from django.test import TestCase
from PIL import Image
import enhancer.image_processor as processor
import enhancer.blur_detection as blur
import enhancer.compressor as comp

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

        comp.compress(test_img_dir, delete_old=False)
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
            comp.compress(test_img_dir, True)
        err = the_error.exception
        self.assertEqual(str(err), "The file images/original2.jpg does not exist.")

    def test_convert_image_to_data_success(self):
        """
        Test to convert an image to base64.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        result = processor.image_to_data(test_img_dir)

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
            processor.image_to_data(test_img_dir)
        err = the_error.exception
        self.assertEqual(str(err),
                         "The file compressed_images/compressed_large2.jpg does not exist.")

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

        processor.data_to_image(img_str, "decoded_image.jpg")
        comp.delete_image("images/decoded_image.jpg")

    @staticmethod
    def test_delete_image_successful():
        """
        Test to delete an image from a directory.
        """
        test_img_dir = "compressed_images/compressed_large.jpg"
        comp.delete_image(test_img_dir)

    def test_delete_image_does_not_exist(self):
        """
        Test when image does not exists return error message.
        """
        test_img_dir = "compressed_images/compressed_large2.jpg"
        with self.assertRaises(Exception) as the_error:
            comp.delete_image(test_img_dir)
        err = the_error.exception
        self.assertEqual(str(err),
                         "The file compressed_images/compressed_large2.jpg does not exist.")

    def test_create_regist_payload_correctly(self):
        """
        Test when payload will be created correctly.
        """
        test_img_dir = "images/SharpHouse.jpg"
        data_str = processor.image_to_data(test_img_dir)

        datas = []
        for _ in range(5):
            datas.append(data_str)
        payload = processor.create_register_payload(datas)

        for i in range(5):
            cur_data = payload["data"][i]["image"]
            self.assertNotEqual(cur_data, "")

    def test_create_regist_payload_datas_length_incorrect(self):
        """
        Test when payload have different lengths.
        """
        test_img_dir = "images/SharpHouse.jpg"
        data_str = processor.image_to_data(test_img_dir)

        datas = []
        for _ in range(4):
            datas.append(data_str)

        with self.assertRaises(Exception) as the_error:
            processor.create_register_payload(datas)
        err = the_error.exception
        self.assertEqual(str(err), "Data length must be 5.")

    def test_create_identification_payload_correctly(self):
        """
        Test when payload will be created correctly.
        """
        test_img_dir = "images/BlurryDavid.jpg"
        data_str = processor.image_to_data(test_img_dir)

        payload = processor.create_identification_payload(data_str)

        cur_data = payload["image"]
        self.assertNotEqual(cur_data, "")

    # ===================== BLUR DETECTION ========================
    def test_image_is_not_blurry(self):
        """
        Test when image is sharp.
        """
        test_img_dir = "images/SharpHouse.jpg"
        self.assertFalse(blur.is_blurry(test_img_dir))

    def test_image_is_blurry(self):
        """
        Test when image is blurry.
        """
        test_img_dir = "images/BlurryDavid.jpg"
        self.assertTrue(blur.is_blurry(test_img_dir))

    # def test_apply_blur_removal_successfully(self):
    #     """
    #     Test when image is blurry will return deblur directory.
    #     """
    #     test_img_dir = "images/BlurryDavid.jpg"
    #     deblur_dir = comp.apply_blur_removal(test_img_dir, delete_old=False)
    #     self.assertEqual(deblur_dir, "blur_removed_images/BlurryDavid.jpg")

    #     comp.delete_image("blur_removed_images/BlurryDavid.jpg")

    # def test_apply_blur_removal_success_with_delete(self):
    #     """
    #     Test when image is blurry will return deblur directory.
    #     """
    #     # Copy Original First
    #     ori_dir = "images/BlurryDavid.jpg"
    #     test_img_dir = "images/BlurryDavid_Copy.jpg"
    #     img = comp.open_image(ori_dir)
    #     img.save(test_img_dir, "JPEG")

    #     deblur_dir = comp.apply_blur_removal(test_img_dir, delete_old=True)
    #     self.assertEqual(deblur_dir, "blur_removed_images/BlurryDavid_Copy.jpg")

    #     comp.delete_image("blur_removed_images/BlurryDavid_Copy.jpg")
