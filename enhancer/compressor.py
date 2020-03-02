"""
Main module for compression.
"""
from io import BytesIO
from PIL import Image
from django.core.files import File

def compress(image_file_dir):
    """
    Function to compress an image from its directory.
    """
    try:
        img = Image.open(image_file_dir)
    except FileNotFoundError:
        ret_msg = "The file " + image_file_dir + " does not exist."
        return ret_msg

    # img_io = BytesIO()
    # img.save(img_io, format='JPEG', optimize=True)

    image_name = image_file_dir.split("/")[-1]
    img.save("compressed_images/compressed_"+image_name,"JPEG",optimize=True,quality=65)
