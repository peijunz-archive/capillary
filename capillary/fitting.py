from numpy import (cov, mean, array, dot, vectorize, arctan2,
                   vstack, sqrt, pi, sin, newaxis, cos, concatenate, cross, inf)
from numpy.linalg import eigh, norm
import warnings
from scipy.optimize import minimize_scalar, minimize
from .edge import G, width
T = 2 * pi / 3


def cov_linearfit(pts, ly=None):
    '''Use points or both lx ly'''
    if ly is not None:
        covm = cov(pts, ly)
        cen = array([mean(pts), mean(ly)])
    else:
        covm = cov(pts)
        cen = mean(pts, axis=1)
    val, vec = eigh(covm)
    idx = val.argsort()
    vec = vec[:, idx]
    return cen, val, vec[1]


def axisdisp(pts, fit_res=None):
    if not fit_res:
        fit_res = cov_linearfit(pts)
    cen, val, direct = fit_res
    dis = dot(pts.transpose() - cen, direct)
    pos = mean([i for i in dis if i > 0])
    neg = mean([i for i in dis if i < 0])
    return vstack([cen + pos * direct, cen + neg * direct]).transpose()


def split(pts, fit_res=None):
    '''Cut points into two groups'''
    if fit_res is None:
        fit_res = cov_linearfit(pts)
    cen, val, direct = fit_res
    vpts = pts.transpose()
    pos = array([i for i in vpts if dot(i - cen, direct) > 0]).transpose()
    neg = array([i for i in vpts if dot(i - cen, direct) < 0]).transpose()
    close = val[1] < 9 * val[0]
    return pos, neg, close


@vectorize
def normalize_angle(t):
    return t % T


@vectorize
def unidiff(x, y):
    p = (x - y) % T
    q = (y - x) % T
    return min(p, q)


def corner(pts, cen=None):
    '''Give a rough estimation of angle'''
    if cen is None:
        cen = mean(pts, axis=1)
    dx, dy = pts - cen[:, newaxis]
    rho = sqrt(dx**2 + dy**2)
    theta = arctan2(dy, dx) % T

    def f(phi):
        return sum((rho * sin(unidiff(theta, phi)))**2)
    res = minimize_scalar(f)
    r = 4 * sqrt(res.fun / len(rho))
    angle = res.x % T
    return array([r, angle])


def init_estimate(pts):
    '''Give a rough estimation of parameters'''
    cen = mean(pts, axis=1)
    cor = corner(pts, cen)
    return concatenate((cen, cor))


def distance(pts, x, rho=None):
    '''Distance between triangle x and points pts'''
    cen = x[:2]
    theta = x[-1]
    if rho is None:
        rho = x[-2]
    rho /= 2
    dis = pts - cen[:, newaxis]
    r = norm(dis, axis=0)
    phi = (arctan2(dis[1], dis[0]) - theta) % T
    return norm(r * (r * cos(phi - T / 2) - rho))


def pdist(pt, x):
    '''Point distance to triangle'''
    cen = x[:2]
    rho, theta = x[2:]
    rho /= 2
    dis = pt - cen
    r = norm(dis, axis=0)
    phi = (arctan2(dis[1], dis[0]) - theta) % T
    dis = r * cos(phi - T / 2) - rho
    return dis


def ds(i, p, n):
    return pdist(i, p) - pdist(i, n)


def resplit(pts, p, n):
    vpts = pts.transpose()
    pos = array([i for i in vpts if ds(i, p, n) < 1]).transpose()
    neg = array([i for i in vpts if ds(i, p, n) > -1]).transpose()
    return pos, neg


def optimize_fit(pts, estimate=None, rho=30):
    '''#TODO enhance code here'''
    if estimate is None:
        estimate = init_estimate(pts)
    if rho is None:
        # Optimize rho
        res = minimize(
            lambda x: distance(pts, x),
            estimate,
            method='BFGS',
        )
        estimate = res.x
    else:
        # Do not optimize rho
        estimate[-2] = estimate[-1]
        res = minimize(
            lambda x: distance(pts, x, rho),
            estimate[:-1],
            method='BFGS',
        )
        estimate[:2] = res.x[:2]
        estimate[-1] = res.x[-1]
        estimate[2] = rho
    err = res.fun / len(pts[0])
    return estimate, err


def double_fit(pts, iterate=3):
    '''Fit points with two triangles'''
    fit_res = cov_linearfit(pts)
    cen, val, direct = fit_res
    pts = array([i for i in pts.transpose() if abs(
        cross(i - cen, direct)) < 40]).transpose()
    pos, neg, close = split(pts, fit_res)
    p, fp = optimize_fit(pos)
    n, fn = optimize_fit(neg)
    if close and iterate:
        for i in range(iterate):
            pos, neg = resplit(pts, p, n)
            p, fp = optimize_fit(pos)
            n, fn = optimize_fit(neg)
    return p, n, pos, neg, fp, fn


def adaptive_fit(video, num, iterate=3):
    '''Adaptive fit frame of a video by changing:
    + Noise and Edge Filter
    + Resplit for close case
    according to the fitting error
    '''
    factor = 1.0
    badness = inf
    bestres = None
    pts_getter = G[video]
    mp, mn = width[video]
    while True:
        pts = pts_getter(num, factor)
        try:
            p, n, pos, neg, fp, fn = double_fit(pts)
        except IndexError:
            warnings.warn("Disturbing edge, with badness {}".format(badness))
            return bestres
        if fp * fn < badness:
            badness = fp * fn
            bestres = (p, n, pos, neg, fp, fn)
        if fp < mp and fn < mn or factor > 1.5:
            break
        factor *= 1.1
    if factor > 1.5:
        warnings.warn("Disturbing edge")
    print(bestres[-2:])
    return bestres


if __name__ == '__main__':
    lx = [0, 0, 1]
    ly = [0, 1, 0]
    print(cov_linearfit(lx, ly))
    # 平均误差
