from skimage.restoration import denoise_tv_chambolle
from skimage.feature import canny
from skimage import io
import numpy as np

edgefilt = np.array([
    [0.05, 1.5],
    [0.08, 1.0],
    [0.09, 1.1],
    [0.15, 1.5],
    [0.13, 1.1],
    [0.1, 1.2],
    [0.15, 1.1],
    [0.13, 1.5]
])


width = np.array([
    [2.7215898398,  2.68920027364],
    [1.74625446383, 1.74625446383],  # 1.65414973627],
    [2.10674968481, 2.0274694363],
    [2.01655262385, 2.05488268876],
    [2.06784274947, 2.09093288310],
    [2.03225926546, 1.99784354101],
    [3.22829341331, 2.75795405483],
    [3.33940193435, 2.84097452172]
])


def upper(a):
    return np.mean(a) + 2.5 * np.std(a)


def loadwidth():
    w = np.empty([8, 2], dtype=float)
    for i in range(8):
        raw = np.load('data/%d.npy' % i)
        fp = raw[:, 0, -1]
        fn = raw[:, 1, -1]
        w[i] = upper(fp), upper(fn)
    print(repr(w))


imgnum = np.array([73, 2956, 1196, 1135, 798, 485, 1463, 1242])


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
        return pts(find(R[n](x), *(k * edgefilt[n])))
    return f


G = [pts_getter(i) for i in range(8)]

if __name__ == "__main__":
    loadwidth()
