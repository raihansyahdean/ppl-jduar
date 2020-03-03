"""
Main module for image processing.
"""
import os
import base64
from io import BytesIO
from PIL import Image
from .compressor import compress

IMAGE_NAMES = ["image_front.jpg", "image_right.jpg",
               "image_left.jpg", "image_bottom.jpg", "image_top.jpg"]

PAYLOAD = {
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
            "position": "bottom",
            "image": ""
        },
        {
            "position": "top",
            "image": ""
        }
    ]
}


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
        data_to_image(datas[i], IMAGE_NAMES[i])
        compress("images/" + IMAGE_NAMES[i])
        delete_image("images/" + IMAGE_NAMES[i])
        compressed_data_str = image_to_data("compressed_images/compressed_" + IMAGE_NAMES[i])
        PAYLOAD["data"][i]["image"] = compressed_data_str

    return PAYLOAD
