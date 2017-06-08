from numpy import arange
import matplotlib.pyplot as plt
from .fitting import *


def show_pts(pts):
    plt.plot(pts[0], pts[1], 'o', markersize=1)


def show_axis(pts):
    res = cov_linearfit(pts)
    xc, yc = displacement(pts, res)
    plt.plot(xc, yc, '--')


def show_split(pos, neg=None):  # BUG
    if neg is None:
        pos, neg = split(pos)
    plt.plot(pos[0], pos[1], 'o', markersize=2, alpha = 0.5)
    plt.plot(neg[0], neg[1], 'o', markersize=2, alpha = 0.5)


def show_hull(x, scale=1):
    xc, yc, r, theta = x
    t = arange(4) * T + theta
    r *= scale
    xl, yl = xc + r * cos(t), yc + r * sin(t)
    plt.plot(xl, yl)


def show_frame(pts, scale=1, iterate = 0):
    # show_axis(pts)
    x1, x2, pos, neg = double_fit(pts, iterate)
    #print(pos, neg)
    #= split(pts)
    #x1, x2 = optimize_fit(pos), optimize_fit(neg)
    show_hull(x1, scale)
    show_hull(x2, scale)
    show_split(pos, neg)
    plt.plot([x1[0], x2[0]], [x1[1], x2[1]], 'o-')
