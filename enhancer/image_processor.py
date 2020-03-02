import os

def delete_image(image_file_dir):
    try:
        os.remove(image_file_dir)
    except FileNotFoundError:
        ret_msg = "The file " + image_file_dir + " does not exist."
        return ret_msg

def data_to_image():
    # lgsg di save ke images folder
    pass

def image_to_data():
    # buka dari compressed_images
    # return text data
    pass

def save_to_json():
    # ngambil data images dari 
    # nge format json
    pass