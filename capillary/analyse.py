from numpy import cumsum, empty, save, arctan2, load, pi, empty_like, diff
from numpy.linalg import norm
import matplotlib.pyplot as plt
from . import edge, fitting
from datetime import datetime


def connectify(l, period):
    '''Minmize the distance between near angles
    with the degree of freedom of periodicity 
    '''
    delta = empty_like(l)
    delta[0] = l[0]
    delta[1:] = (diff(l) + period / 2) % period - period / 2
    return cumsum(delta)


def action(video, frame_list, cachefile=None):
    '''Analyse frames of a video and save it into cache'''
    res = empty([len(frame_list), 2, 5])
    for i, frame in enumerate(frame_list):
        p, n, _, _, fp, fn = fitting.adaptive_fit(video, frame)
        print(i, p, n)
        res[i, 0, :4] = p
        res[i, 0, 4] = fp
        res[i, 1, :4] = n
        res[i, 1, 4] = fn
    if cachefile is None:
        cachefile = str(datetime.now()) + '.npy'
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


def analyse_raw(raw):
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


def analyse_frames(video, frame_list, flush=False, cachefile='measured_res.npy'):
    return analyse_raw(rawres(video, frame_list, flush, cachefile))


def process_raw(i):
    pts = edge.G[0](i + 1)
    print(fitting.double_fit(pts))


def analyse_video(i):
    action(i, range(1, edge.img_num[i] + 1), cachefile='data/{}.npy'.format(i))


if __name__ == "__main__":
    from multiprocessing import Pool
    p = Pool()
    p.map(analyse_video, range(5, 6))
    p.close()
    p.join()
