"""
Main module for image processing.
"""
import os
import base64
from io import BytesIO
from PIL import Image

def delete_image(image_file_dir):
    """
    Function to delete an image from its directory.
    """
    try:
        os.remove(image_file_dir)
        return "delete successful"
    except FileNotFoundError:
        ret_msg = "The file " + image_file_dir + " does not exist."
        return ret_msg

def data_to_image(data, image_name):
    """
    Function to convert image data to image and save it.
    """
    img = Image.open(BytesIO(base64.b64decode(data)))
    img.save('images/' + image_name, 'JPEG')
    return "Successful convert to images/" + image_name

def image_to_data(image_file_dir):
    """
    Function to convert an image to a data image.
    """
    try:
        image = Image.open(image_file_dir)
    except FileNotFoundError:
        message = "File " + image_file_dir + " not found."
        return message

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

def save_to_json():
    """
    Function to save images to json format ready to be sent.
    """
    # ngambil data images dari
    # nge format json
    pass
