from numpy import cumsum, empty, save, arctan2, load, pi, empty_like, diff
from numpy.linalg import norm
import matplotlib.pyplot as plt
from . import edge, fitting, display
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
    Res = empty([len(frame_list), 2, 5])
    for i, frame in enumerate(frame_list):
        p, n, _, _, fp, fn = fitting.adaptive_fit(video, frame)
        print(i, p, n)
        Res[i, 0, :4] = p
        Res[i, 0, 4] = fp
        Res[i, 1, :4] = n
        Res[i, 1, 4] = fn
    if cachefile is None:
        cachefile = str(datetime.now()) + '.npy'
    save(cachefile, Res)
    return Res


def rawres(video, frame_list, flush, cachefile):
    '''Get raw result of both particles from frames'''
    if flush:
        Res = action(video, frame_list, cachefile)
    else:
        try:
            Res = load(cachefile)
        except FileNotFoundError:
            Res = action(video, frame_list, cachefile)
    return Res


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


def analyse(video, frame_list, flush=False, cachefile='measured_res.npy'):
    return analyse_raw(rawres(video, frame_list, flush, cachefile))


def process_svg(i):
    plt.clf()
    print('Processing frame %d' % (i + 1))
    pts = edge.G[0](i + 1)
    display.show_frame(pts)
    # grid();
    plt.axis('square')
    #plt.xlim(0, 284)
    #plt.ylim(0, 284)
    plt.savefig('processed/output_%04d_processed.svg' % (i + 1),
                bbox_inches='tight',
                )


def process_raw(i):
    pts = edge.G[0](i + 1)
    print(fitting.double_fit(pts))


if __name__ == "__main__":
    for i in range(1, 8):
        action(i, range(
            1, edge.imgnum[i] + 1, edge.imgnum[i] // 200),   cachefile='data/%d.npy' % i)
    #from multiprocessing import Pool
    # p=Pool()
    #p.map(process_raw, range(73))
    # p.close()
    # p.join()
