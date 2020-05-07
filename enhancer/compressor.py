"""
Main module for compression.
"""
import os
from PIL import Image
import enhancer.blur_detection as bd

BLUR_DIR = "blur_removed_images/"

def open_image(image_file_dir):
    """
    Function to open an image from its directory.
    """
    try:
        img = Image.open(image_file_dir)
    except FileNotFoundError:
        err_msg = "The file " + image_file_dir + " does not exist."
        raise Exception(err_msg)

    return img

def delete_image(image_file_dir):
    """
    Function to delete an image from its directory.
    """
    try:
        os.remove(image_file_dir)
    except FileNotFoundError:
        err_msg = "The file " + image_file_dir + " does not exist."
        raise Exception(err_msg)


def compress(image_file_dir, delete_old=True):
    """
    Function to compress an image from its directory.
    """
    img = open_image(image_file_dir)

    image_name = image_file_dir.split("/")[-1]
    img.save("compressed_images/compressed_"+image_name, "JPEG", optimize=True, quality=65)

    if delete_old:
        delete_image(image_file_dir)

    return "compressed_images/compressed_"+image_name

def apply_blur_removal(image_file_dir, delete_old=True):
    """
    Function to remove blur from images.
    If images is not blur, it is not changed.
    Saves the image into a directory.
    Return is the image file directory of the new image.
    """

    return image_file_dir
