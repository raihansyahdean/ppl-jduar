import sys
from io import BytesIO
from PIL import Image
from django.core.files import File

# Function to compress an image from its directory
def compress(image_file_dir):
    img = Image.open(image_file_dir)
    img_io = BytesIO()
    img.save(img_io, format = 'JPEG', optimize = True)
    new_image = File(img_io, name = image_file_dir.split("/")[-1])

    return new_image
