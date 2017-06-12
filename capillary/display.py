from numpy import sin, cos, arange
import matplotlib.pyplot as plt
from . import fitting, edge
from .fitting import T, adaptive_fit, double_fit
from multiprocessing import Pool
from functools import partial


def show_pts(pts):
    plt.plot(pts[0], pts[1], 'o', markersize=1)


def show_axis(pts):
    res = cov_linearfit(pts)
    xc, yc = axis_displace(pts, res)
    plt.plot(xc, yc, '--')


def show_split(pos, neg=None):  # BUG
    if neg is None:
        pos, neg = split(pos)
    plt.plot(pos[0], pos[1], 'o', markersize=2, alpha=0.5)
    plt.plot(neg[0], neg[1], 'o', markersize=2, alpha=0.5)


def show_hull(x, scale=1):
    '''Show fitting triangles'''
    xc, yc, r, theta = x
    t = arange(4) * T + theta
    r *= scale
    xl, yl = xc + r * cos(t), yc + r * sin(t)
    plt.plot(xl, yl)


def show_frame(v, frame, save=True, fmt='pdf'):
    '''Show the split of points and hulls for a frame'''
    plt.clf()
    x1, x2, pos, neg, fp, fn = adaptive_fit(v, frame)
    show_hull(x1, 1)
    show_hull(x2, 1)
    show_split(pos, neg)
    plt.plot([x1[0], x2[0]], [x1[1], x2[1]], 'o-')
    plt.axis('equal')
    plt.title('Video {}, Frame {}'.format(v, frame))
    if save:
        print('Processing video {} frame {}...'.format(v, frame))
        plt.savefig('{0}/{1}/output_{2:04}_processed.{0}'.format(fmt, v, frame),
                    bbox_inches='tight',
                    )


def visualize_frames(v, frames, multi=True):
    if multi:
        p = Pool()
        func = partial(show_frame, v)
        p.map(func, frames)
        p.close()
        p.join()
    else:
        for frame in frames:
            singles_frame(frame)

from itertools import chain

def visualize_video(v, start=1, step=5):
    l1=range(start, edge.touch[v]-step, step)
    l2=range(edge.touch[v]-step, edge.img_num[v]+1)
    visualize_frames(v, chain(l1, l2))


if __name__ == "__main__":
    #visualize_frames(6, range(1440, 1464, 20))
    visualize_video(1, step=20)
