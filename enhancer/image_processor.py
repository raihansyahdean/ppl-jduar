"""
Main module for image processing.
"""
import os
import base64
from io import BytesIO
from PIL import Image
from .compressor import compress

COMPRESSED_DIR = "compressed_images/compressed_"

IMAGE_DIR = "images/"

REGISTRATION_IMAGE_NAMES = ["image_front.jpg", "image_right.jpg",
                            "image_left.jpg", "image_top.jpg", "image_bottom.jpg"]

REGIST_PAYLOAD_TEMPLATE = {
    "data": [
        {
            "position": "front",
            "image": ""
        },
        {
            "position": "right",
            "image": ""
        },
        {
            "position": "left",
            "image": ""
        },
        {
            "position": "top",
            "image": ""
        },
        {
            "position": "bottom",
            "image": ""
        }
    ]
}

IDENTIFICATION_PAYLOAD_TEMPLATE = {
    "image": ""
}

IDENTIFICATION_IMAGE_NAME = "identify_image.jpg"

def delete_image(image_file_dir):
    """
    Function to delete an image from its directory.
    """
    try:
        os.remove(image_file_dir)
    except FileNotFoundError:
        err_msg = "The file " + image_file_dir + " does not exist."
        raise Exception(err_msg)

def data_to_image(data, image_name):
    """
    Function to convert image data to image and save it.
    """
    img = Image.open(BytesIO(base64.b64decode(data)))
    img.save('images/' + image_name, 'JPEG')

def image_to_data(image_file_dir):
    """
    Function to convert an image to a data image.
    Returns base64 string of image.
    """
    try:
        image = Image.open(image_file_dir)
    except FileNotFoundError:
        err_msg = "File " + image_file_dir + " not found."
        raise Exception(err_msg)

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

def create_register_payload(datas):
    """
    Function to save images to json format ready to be sent.
    Datas is an array with 5 original images in base64 format.
    Returns complete payload.
    """
    if len(datas) != 5:
        err_msg = "Data length must be 5."
        raise Exception(err_msg)

    for i in range(5):
        data_to_image(datas[i], REGISTRATION_IMAGE_NAMES[i])
        compress(IMAGE_DIR + REGISTRATION_IMAGE_NAMES[i])
        delete_image(IMAGE_DIR + REGISTRATION_IMAGE_NAMES[i])
        compressed_data_str = image_to_data(COMPRESSED_DIR + REGISTRATION_IMAGE_NAMES[i])
        compressed_data_str = str(compressed_data_str)
        REGIST_PAYLOAD_TEMPLATE["data"][i]["image"] = compressed_data_str
        delete_image(COMPRESSED_DIR + REGISTRATION_IMAGE_NAMES[i])

    return REGIST_PAYLOAD_TEMPLATE

def create_identification_payload(image_str):
    """
    Function to save identification image to json format ready to be sent.
    Datas is an image in base64 format.
    Returns complete payload.
    """

    data_to_image(image_str, IDENTIFICATION_IMAGE_NAME)
    compress(IMAGE_DIR + IDENTIFICATION_IMAGE_NAME)
    delete_image(IMAGE_DIR + IDENTIFICATION_IMAGE_NAME)
    compressed_data_str = image_to_data(COMPRESSED_DIR + IDENTIFICATION_IMAGE_NAME)
    compressed_data_str = str(compressed_data_str)
    IDENTIFICATION_PAYLOAD_TEMPLATE["image"] = compressed_data_str
    delete_image(COMPRESSED_DIR + IDENTIFICATION_IMAGE_NAME)

    return IDENTIFICATION_PAYLOAD_TEMPLATE
