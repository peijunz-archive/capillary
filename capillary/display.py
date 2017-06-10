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


def show_frame(v, frame, save=True):
    '''Show the split of points and hulls for a frame'''
    plt.clf()
    x1, x2, pos, neg, fp, fn = adaptive_fit(v, frame)
    show_hull(x1, 1)
    show_hull(x2, 1)
    show_split(pos, neg)
    plt.plot([x1[0], x2[0]], [x1[1], x2[1]], 'o-')
    plt.axis('equal')
    if save:
        print('Processing video {} frame {}:'.format(v, frame))
        plt.savefig('SVG/{}/output_{:04}_processed.svg'.format(v, frame),
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


def visualize_video(v, start=1, step=1):
    visualize_frames(v, range(start, edge.img_num[v] + 1, step))


if __name__ == "__main__":
    visualize_video(1, start=1900)
