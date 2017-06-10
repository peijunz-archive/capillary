# Infrastructure for video analysis
# Edge Detection and magical parameters

from skimage.restoration import denoise_tv_chambolle
from skimage.feature import canny
from skimage import io
import numpy as np

edge_filt = np.array([
    [0.05, 1.5],
    [0.08, 1.0],
    [0.06, 1.0],
    [0.1, 1],
    [0.1, 1.1],
    [0.1, 1.2],
    [0.1, 1],
    [0.3, 0.3]
])


width = np.array([
    [2.67648717,  2.60988034],
    [2.1,  2.1],
    [2.2,  2.2],
    [2.2,  2.2],
    [2.2,  2.2],
    [2.2,  2.2],
    [3.14315619,  2.68117912],
    [3.14290475,  2.60330584]
])

lv = np.array([0, 3, 5, 5, 0, 0, ])


def load_width():
    w = np.empty([8, 2], dtype=float)
    for i in range(8):
        raw = np.load('data/%d.npy' % i)
        fp = raw[:, 0, -1]
        fn = raw[:, 1, -1]
        w[i] = np.percentile(fp, 95), np.percentile(fn, 95)
    return w


img_num = np.array([73, 2956, 1196, 1135, 798, 485, 1463, 1242])


def find(im, weight=0.05, sigma=1.5):
    '''Donoise first, and then use canny filter to find edge
    weight  used for denoise_tv_chambolle
    sigma   used for edge
    '''
    if weight:
        im = denoise_tv_chambolle(im, weight=weight, multichannel=True)
    if sigma:
        im = canny(im, sigma=sigma)
    return im


def pts(im):
    '''Extract coordinates of edges'''
    return np.array(np.nonzero(im))


img_path = "/home/zpj/code/capillary/images/%d/"
img_name = "output_%04d.png"


def image_reader(path, name):
    return lambda s: io.imread(path + name % s, as_grey=True)


R = [image_reader(img_path % i, img_name) for i in range(8)]


def pts_getter(n):
    def f(x, k=1):
        return pts(find(R[n](x), *(k * edge_filt[n])))
    return f


G = [pts_getter(i) for i in range(8)]

if __name__ == "__main__":
    print(load_width())
