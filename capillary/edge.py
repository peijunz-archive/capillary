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
    return np.array(np.nonzero(im))


def image_reader(fmt="images/output_%04d.png"):
    return lambda s: io.imread(fmt % s, as_grey=True)


def get(n):
    R = image_reader()
    return pts(find(R(n)))


if __name__ == "__main__":
    R = image_reader()
    print(R(1))
