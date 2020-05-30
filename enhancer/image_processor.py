"""
Main module for image processing.
"""
import base64
import ctypes 
import threading
from io import BytesIO
from PIL import Image
import enhancer.compressor as comp

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

BAD_IMAGE_FLAG = False

class ImageThread(threading.Thread):
    """
    Class for image threading (registration photo processing)
    """
    def __init__(self, filename, image_dir, thread_id):
        threading.Thread.__init__(self)
        self.filename = filename
        self.image_dir = image_dir
        self.thread_id = thread_id
        self.BAD_IMAGE_FLAG = False

    def run(self):
        try:
            blur_removed_dir = comp.apply_blur_removal(self.image_dir + self.filename, delete_old=True)
        except:
            # Reject Image
            self.raise_exception()

        compress_dir = comp.compress(blur_removed_dir, delete_old=True)

        # Creating Payload
        compressed_data_str = image_to_data(compress_dir)
        compressed_data_str = str(compressed_data_str)
        REGIST_PAYLOAD_TEMPLATE["data"][self.thread_id]["image"] = compressed_data_str
        comp.delete_image(compress_dir)
    
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def raise_exception(self):
        self.BAD_IMAGE_FLAG = True
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

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
    image = comp.open_image(image_file_dir)

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
    BAD_IMAGE_FLAG = False
    threads = []
    if len(datas) != 5:
        err_msg = "Data length must be 5."
        raise Exception(err_msg)

    for i in range(5):
        data_to_image(datas[i], REGISTRATION_IMAGE_NAMES[i])
        # Multithreading to process faster
        image_thread = ImageThread(REGISTRATION_IMAGE_NAMES[i], IMAGE_DIR, i)
        image_thread.start()
        threads.append(image_thread)

    for thread in threads:
        thread.join()

    BAD_IMAGE_FLAG = threads[0].BAD_IMAGE_FLAG

    if BAD_IMAGE_FLAG:
        # Bad Image Sent
        BAD_IMAGE_FLAG = False
        err_msg = "Bad Image Sent"
        raise Exception(err_msg)

    return REGIST_PAYLOAD_TEMPLATE

def create_identification_payload(image_str):
    """
    Function to save identification image to json format ready to be sent.
    Datas is an image in base64 format.
    Returns complete payload.
    """

    data_to_image(image_str, IDENTIFICATION_IMAGE_NAME)
    try:
        blur_removed_dir = comp.apply_blur_removal(IMAGE_DIR + IDENTIFICATION_IMAGE_NAME, delete_old=True)
    except:
        # Reject Image
        err_msg = "Bad Image Sent"
        raise Exception(err_msg)

    compress_dir = comp.compress(blur_removed_dir, delete_old=True)

    # Creating Payload
    compressed_data_str = image_to_data(compress_dir)
    compressed_data_str = str(compressed_data_str)
    IDENTIFICATION_PAYLOAD_TEMPLATE["image"] = compressed_data_str
    comp.delete_image(compress_dir)

    return IDENTIFICATION_PAYLOAD_TEMPLATE
