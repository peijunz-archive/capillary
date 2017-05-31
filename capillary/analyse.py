from numpy import cumsum, empty, save, arctan2, load, pi, empty_like, diff
from numpy.linalg import norm
import matplotlib.pyplot as plt
from . import *


def connectify(l, period):
    '''Minmize the distance between near angles
    with the degree of freedom of periodicity 
    '''
    delta = empty_like(l)
    delta[0] = l[0]
    delta[1:] = (diff(l) + period / 2) % period - period / 2
    return cumsum(delta)


def rawres(pts_getter, frame_list):
    '''Get raw result of both particles from frames'''
    cachefile = 'measured_result.npy'
    try:
        # Load cached result
        Res = load(cachefile)
    except FileNotFoundError:
        Res = empty([len(frame_list), 2, 4])
        for i, frame in enumerate(frame_list):
            pts = pts_getter(frame)
            pos, neg = fitting.split(pts)
            Res[i, 0] = fitting.optimize_fit(pos)
            Res[i, 1] = fitting.optimize_fit(neg)
        save(cachefile, Res)
    return Res


def analyse_raw(raw):
    '''Analyse raw result and get (rho, theta) for displacement and
    orientation of each one'''
    cen = raw[:, 0, :2] - raw[:, 1, :2]
    rho = norm(cen, axis=1)
    theta = connectify(arctan2(cen[:, 1], cen[:, 0]), 2 * pi)
    t1 = connectify(raw[:, 0, 3], 2 * pi / 3)
    t2 = connectify(raw[:, 1, 3], 2 * pi / 3)
    return rho, theta, t1, t2


def analyse(pts_getter, frame_list):
    return analyse_raw(rawres(pts_getter, frame_list))


def process_svg():
    for i in range(73):
        plt.clf()
        print('Processing frame %d' % (i + 1))
        pts = edge.get(i + 1)
        display.show_frame(pts)
        # grid();
        plt.axis('square')
        plt.xlim(0, 284)
        plt.ylim(0, 284)
        plt.savefig('processed/output_%04d_processed.svg' % (i + 1),
                    bbox_inches='tight',
                    )


if __name__ == "__main__":
    process_svg()
