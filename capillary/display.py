from numpy import arange
import matplotlib.pyplot as plt
from .fitting import *


def show_pts(pts):
    plt.plot(pts[0], pts[1], 'o', markersize=1)


def show_displace(pts):
    res = cov_linearfit(pts)
    xc, yc = displacement(pts, res)
    plt.plot(xc, yc, 'r-')


def show_split(pos, neg=None):
    if neg is None:
        pos, neg = split(pts)
    plt.plot(pos[0], pos[1], 'o', markersize=1)
    plt.plot(neg[0], neg[1], 'o', markersize=1)


def show_hull(pts):
    xc, yc = mean(pts, axis=1)
    r, theta = corner(pts)
    t = arange(4) * T + theta
    r *= 1.4
    xl, yl = xc + r * cos(t), yc + r * sin(t)
    plt.plot(xl, yl)


def show_frame(pts):
    pos, neg = split(pts)
    show_hull(pos)
    show_hull(neg)
    show_split(pos, neg)
    show_displace(pts)
