"""
Main module for blur detection (library)
Source: https://github.com/indyka/blur-detection
"""
# import the necessary packages
import cv2

def variance_of_laplacian(image):
    """
        Calculate the variance of laplacian from image matrix
        :param image: image matrix
        :return: laplacian
    """
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


def is_blurry(image_directory):
    """
        Image blurry checker
        :param image_directory: directory of converted image
        :return: boolean of blur result
    """
    image = cv2.imread(image_directory)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = variance_of_laplacian(gray)
    print("[BLUR_VARIANCE] " + str(variance))
    return variance
