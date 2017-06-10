from numpy import arange
import matplotlib.pyplot as plt
from .fitting import *
from .edge import *


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
    xc, yc, r, theta = x
    t = arange(4) * T + theta
    r *= scale
    xl, yl = xc + r * cos(t), yc + r * sin(t)
    plt.plot(xl, yl)


def show_frame(pts, scale=1, iterate=0):
    # show_axis(pts)
    x1, x2, pos, neg, fp, fn = double_fit(pts, iterate)
    #print(pos, neg)
    #= split(pts)
    #x1, x2 = optimize_fit(pos), optimize_fit(neg)
    show_hull(x1, scale)
    show_hull(x2, scale)
    show_split(pos, neg)
    plt.plot([x1[0], x2[0]], [x1[1], x2[1]], 'o-')


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


def visualize_svg(v, frames):
    for i, frame in enumerate(frames):
        plt.clf()
        x1, x2, pos, neg, fp, fn = adaptive_fit(v, frame, lv=5)
        show_hull(x1, 1)
        show_hull(x2, 1)
        show_split(pos, neg)
        plt.plot([x1[0], x2[0]], [x1[1], x2[1]], 'o-')
        plt.axis('equal')
        print('Processing video %d frame %d' % (v, frame))
        plt.savefig('SVG/%d/output_%04d_processed.svg' % (v, frame),
                    bbox_inches='tight',
                    )


if __name__ == "__main__":
    visualize_svg(7, range(200, img_num[7] + 1, 20))
