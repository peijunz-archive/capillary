from numpy import (cov, mean, array, dot, vectorize, arctan2,
                   vstack, sqrt, pi, sin, newaxis, cos, concatenate)
from numpy.linalg import eigh, norm
import warnings
from scipy.optimize import minimize_scalar, minimize

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


def displacement(pts, fit_res=None):
    if not fit_res:
        fit_res = cov_linearfit(pts)
    cen, val, direct = fit_res
    dis = dot(pts.transpose() - cen, direct)
    pos = mean([i for i in dis if i > 0])
    neg = mean([i for i in dis if i < 0])
    return vstack([cen + pos * direct, cen + neg * direct]).transpose()


def split(pts, fit_res = None, silent = False):
    '''If separation is large, cut into two point groups'''
    if not fit_res:
        fit_res = cov_linearfit(pts)
    cen, val, direct = fit_res
    pos = array([i for i in pts.transpose() if dot(
        i - cen, direct) >= 0]).transpose()
    neg = array([i for i in pts.transpose() if dot(
        i - cen, direct) < 0]).transpose()
    close = val[1] < 9 * val[0]
    if not silent:
        if close:
            warnings.warn("Particles are too close, separation may fail!")
        return pos, neg
    else:
        return pos, neg, close


def resplit(pts, p, n):
    pos = array([i for i in pts.transpose() if pdist(i, p) - pdist(i, n) < 1]).transpose()
    neg = array([i for i in pts.transpose() if pdist(i, p) - pdist(i, n) > -1]).transpose()
    return pos, neg


def position(pts):
    pos, neg = split(pts)
    x1 = optimize_fit(pos)
    x2 = optimize_fit(neg)
    return x1, x2


@vectorize
def normalize_angle(t):
    return t % T


@vectorize
def unidiff(x, y):
    p = (x - y) % T
    q = (y - x) % T
    return min(p, q)


def corner(pts, cen=None):
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
    # theta=(theta-res.x)%T
    #a, b, dirc=cov_linearfit(rho*cos(theta), rho*sin(theta))
    #angle2=arctan2(dirc[1], dirc[0])%T
    #print(res.x, angle2, (res.x-angle2)%T)
    return array([r, angle])


def init_estimate(pts):
    cen = mean(pts, axis=1)
    cor = corner(pts, cen)
    return concatenate((cen, cor))


def distance(pts, x):
    cen = x[:2]
    rho, theta = x[2:]
    rho /= 2
    if len(pts.shape) == 1:
        dis = pts - cen
    else:
        dis = pts - cen[:, newaxis]
    r = norm(dis, axis=0)
    phi = (arctan2(dis[1], dis[0]) - theta) % T
    return norm(r * (r * cos(phi - T / 2) - rho))


def pdist(pt, x):
    cen = x[:2]
    rho, theta = x[2:]
    rho /= 2
    dis = pt - cen
    r = norm(dis, axis=0)
    phi = (arctan2(dis[1], dis[0]) - theta) % T
    dis = r * cos(phi - T / 2) - rho
    return dis


#def pdistance(p, x):
    
    #r=norm(p)
    #phi=arctan2(dis[1], dis[0])-x[]


def optimize_fit(vpts, estimate=None):
    if estimate is None:
        estimate = init_estimate(vpts)
    res = minimize(
        lambda x: distance(vpts, x),
        estimate,
        method='BFGS',
    )
    return res.x


def double_fit(pts, iterate = 3):
    pos, neg, close = split(pts, silent=True)
    p, n = optimize_fit(pos), optimize_fit(neg)
    #return p, n, pos, neg
    if close and iterate:
        for i in range(iterate):
            pos, neg = resplit(pts, p, n)
            p, n = optimize_fit(pos, p), optimize_fit(neg, n)
    return p, n, pos, neg


if __name__ == '__main__':
    lx = [0, 0, 1]
    ly = [0, 1, 0]
    print(cov_linearfit(lx, ly))
