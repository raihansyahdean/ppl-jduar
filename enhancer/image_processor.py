"""
Main module for image processing.
"""
import os

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

def data_to_image():
    """
    Function to convert image data to image and save it.
    """
    # lgsg di save ke images folder
    pass

def image_to_data():
    """
    Function to convert an image to a data image.
    """
    # buka dari compressed_images
    # return text data
    pass

def save_to_json():
    """
    Function to save images to json format ready to be sent.
    """
    # ngambil data images dari
    # nge format json
    pass
