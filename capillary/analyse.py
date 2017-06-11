from numpy import (cumsum, empty, save, load, arctan2, load, pi, empty_like,
                   diff, vectorize, round, mean)
from numpy.linalg import norm
import matplotlib.pyplot as plt
from . import edge, fitting
from datetime import datetime
import pandas as pd
from collections import OrderedDict


@vectorize
def absmin(t, T):
    return (t + T / 2) % T - T / 2


def regularize(l, period, k=10):
    std = mean(l[-6:])
    n = (absmin(std, period) - std) / period
    return l + n * period


def connectify(l, period):
    '''Minimize the distance between near angles
    with the degree of freedom of periodicity 
    '''
    delta = empty_like(l)
    delta[0] = l[0]
    delta[1:] = absmin(diff(l), period)
    return cumsum(delta)


def action(video, frame_list, cachefile=None):
    '''Analyse frames of a video and save it into cache'''
    res = empty([len(frame_list), 11], dtype=float)
    for i, frame in enumerate(frame_list):
        p, n, _, _, fp, fn = fitting.adaptive_fit(video, frame)
        #print(i, frame, p, n)
        res[i, :4] = p
        res[i, 4] = fp
        res[i, 5:9] = n
        res[i, 9] = fn
        res[i, 10] = frame
    if cachefile is None:
        cachefile = str(datetime.now()) + '.npy'
    try:
        df1 = pd.DataFrame(load(cachefile))
        df2 = pd.DataFrame(res)
        n1 = old.shape[0]
        n2 = res.shape[0]
        df = pd.concat((df1, df2)).drop_duplicates(subset=10, keep="last")
        res = df.sort_values([10]).as_matrix()
        print(
            "Merging {} old + {} new --> {} total".format(n1, n2, res.shape[0]))
    except FileNotFoundError:
        print("Creating cache file {}".format(cachefile))
    save(cachefile, res)
    return res


def rawres(video, frame_list, flush, cachefile):
    '''Get raw result of both particles from frames'''
    if flush:
        res = action(video, frame_list, cachefile)
    else:
        try:
            res = load(cachefile)
        except FileNotFoundError:
            res = action(video, frame_list, cachefile)
    return res


def analyse_raw_old(raw):
    '''Analyse raw result and get (rho, theta) for displacement and
    orientation of each one'''
    cen = raw[:, 1, :2] - raw[:, 0, :2]
    rho = norm(cen, axis=1)
    theta = connectify(arctan2(cen[:, 1], cen[:, 0]), 2 * pi)
    t1 = connectify(raw[:, 0, 3], 2 * pi / 3)
    t2 = connectify(raw[:, 1, 3], 2 * pi / 3)
    fp = raw[:, 0, -1]
    fn = raw[:, 1, -1]
    return rho, theta, t1, t2, fp, fn


def analyse_raw(n):
    '''Analyse raw result and get (rho, theta) for displacement and
    orientation of each one'''
    raw = load('data/{}.npy'.format(n))
    cols = ['x1', 'y1', 'r1', 'phi1', 'err1',
            'x2', 'y2', 'r2', 'phi2', 'err2']
    T = pi / 3 * 2
    r1 = raw[:, :2]
    r2 = raw[:, 5:7]
    r21 = r2 - r1
    phi1 = connectify(raw[:, 3], T)
    phi2 = connectify(raw[:, 8], T)
    fp = raw[:, 4]
    fn = raw[:, 9]
    rho = norm(r21, axis=1)
    theta21 = connectify(arctan2(r21[:, 1], r21[:, 0]), 2 * pi)
    theta12 = theta21 + pi
    theta1 = regularize(phi1 - theta21, T)
    theta2 = regularize(phi2 - theta12, T)
    frames = raw[:, 10]
    t = (frames - edge.touch[n]) / edge.frate[n]
    data = OrderedDict([
        #('frame', frames),
        ('time', t),
        ('x1', r1[:, 0]),
        ('y1', r1[:, 1]),
        ('phi1', phi1),
        ('err1', fp),
        ('x2', r2[:, 0]),
        ('y2', r2[:, 1]),
        ('phi2', phi2),
        ('err2', fn),
        ('rho', rho),
        ('theta21', theta21),
        ('theta1', theta1),
        ('theta2', theta2),
    ])
    df = pd.DataFrame(data, columns=data.keys())
    df.index = frames.astype(int)
    df.index.name = 'Frame'
    df = df[df['err1'] < 2 * edge.width[n][0]]
    df = df[df['err2'] < 2 * edge.width[n][1]]
    return df


def to_excel(l):
    writer = pd.ExcelWriter('output.xlsx')
    for i in l:
        df = analyse_raw(i)
        df.to_excel(writer, 'Video {}'.format(i))
    writer.save()


def analyse_frames(video, frame_list, flush=False, cachefile='measured_res.npy'):
    return analyse_raw(rawres(video, frame_list, flush, cachefile))


def process_raw(i):
    pts = edge.G[0](i + 1)
    print(fitting.double_fit(pts))


def analyse_video(v):
    action(v, range(1, edge.img_num[v] + 1), cachefile='data/{}.npy'.format(v))


if __name__ == "__main__":
    #from multiprocessing import Pool
    #p = Pool()
    #p.map(analyse_video, range(3, 4))
    # p.close()
    # p.join()
    action(3, range(59, 61), cachefile='test.npy')
