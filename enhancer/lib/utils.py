import numpy as np
# import time
from .tifffile import imsave
from os.path import join

def uniform_kernel(size):
    kern = np.ones((size, size))
    kern /= np.sum(kern)
    return kern


def save(pic, name, dest_path):
    # tiff = TIFF.open(, mode='w')

    # For compatibility with PIL, we have to roll the 3rd and first axis.
    # PIL opens RGB images with RGB channels on the 3rd dimension
    # libtiff opens RGB images with RGB channels on the first dimension
    # tiff.write_image(np.rollaxis(pic, 2), compression='lzw', write_rgb=True)
    # tiff.close()

    imsave(join(dest_path, name + ".jpg"), pic.astype(np.uint16), dtype=np.uint16, photometric='rgb')


# def timeit(method):
#     '''
#     From: http://www.samuelbosch.com/2012/02/timing-functions-in-python.html
#     '''

#     def timed(*args, **kw):
#         ts = time.time()
#         result = method(*args, **kw)
#         te = time.time()

#         print('%r %2.2f sec' % (method.__name__, te - ts))
#         return result

#     return timed
