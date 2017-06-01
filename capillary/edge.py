from skimage.restoration import denoise_tv_chambolle
from skimage.feature import canny
from skimage import io
import numpy as np


def find(im, weight=0.05, sigma=1.5):
    '''Donoise first, and then use canny filter to find edge
    weight  used for denoise_tv_chambolle
    sigma   used for edge
    '''
    im2 = denoise_tv_chambolle(im, weight=0.05, multichannel=True)
    return canny(im2, sigma=1.5)


def pts(im):
    '''Extract coordinates of edges'''
    return np.array(np.nonzero(im))


def image_reader(fmt):
    return lambda s: io.imread(fmt % s, as_grey=True)


R = image_reader("/home/zpj/code/capillary/images/output_%04d.png")


def get(n, reader=R):
    return pts(find(reader(n)))


if __name__ == "__main__":
    print(R(1))
