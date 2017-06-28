from capillary import edge, fitting, analyse, display
from pylab import *
rc('text', usetex=True)
df0=[analyse.analyse_raw(i) for i in range(0, 8)]
# Three subplots sharing both x/y axes

def draw(kind='mirror', start=10):
    cla()
    dfs=[i.loc[i['time']>-start] for i in df0]
    nrow = 2
    f, ax = plt.subplots(nrow, 2, sharex=True)
    #ax[0, 0].axvline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    #ax[0, 1].axvline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    #ax[1, 1].axvline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    #ax[1, 0].axvline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    #ax[1, 1].axhline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    #ax[1, 0].axhline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[0, 1])

    ax[1, 0].set_yticks([-pi/3, -pi/6, 0, pi/6, pi/3])
    ax[1, 1].set_yticks([-pi/3, -pi/6, 0, pi/6, pi/3])
    ax[1, 0].set_yticklabels([r'$-\frac{\pi}{3}$', r'$-\frac{\pi}{6}$', r'$0$', r'$\frac{\pi}{6}$', r'$\frac{\pi}{3}$'])
    ax[1, 1].set_yticklabels([])
    ax[0, 1].set_yticklabels([])

    ax[1, 1].get_shared_y_axes().join(ax[1, 0], ax[1, 1])

    # TIP-TIP

    cols = (r'$\textrm{tip-tip}$', r'$\textrm{tip-side}$')
    for i, col in enumerate(cols):
        ax[0, i].set_title(col, fontsize=10)
    rows = (r'$r$', r'$\theta_1, \theta_2$', r'$\theta_1, \theta_2$')[:nrow]
    for i, row in enumerate(rows):
        ax[i, 0].set_ylabel(row, fontsize=10, rotation=0)


    tt=[(3, 'o'), (4, 's'), (5, '>'), (7, '^')]
    ts=[(1, 'o'), (2, 's'), (6, '^')]

    l=[(*i, 0) for i in tt] + [(*i, 1) for i in ts]

    iax = [f.add_axes([.14, .62, .15, .15]), 
        f.add_axes([.54, .64, .15, .13])]
    alp=1
    for i, m, typ in l:
        df = dfs[i]
        dfp = df.loc[df['time']<0]
        ax[0, typ].scatter(dfp['time'], dfp['rho'], s=1, marker=m, label=r"${}$".format(i), alpha=alp, lw = 0)
        iax[typ].scatter(log(-dfp['time']), log(dfp['rho']), s=1, marker=m, alpha=alp, lw = 0)
        ax[1, typ].scatter(df['time'], df['theta1'], s=1, marker=m, label=r"$\theta_1, {}$".format(i), alpha=alp, lw = 0)
        #ax[1, typ].plot(df['time'], (-1)**(1+0)*df['theta2'], m, markersize=1, label=r"${}\ \theta_2$".format(i))
        if kind == 'mirror' or not typ:
            lab2=r"$\theta_2, {}$".format(i)
            sign=1
        else:
            lab2=r"$\vartheta_2, {}$".format(i)
            sign=-1
        ax[1, typ].scatter(df['time'], -sign*df['theta2'], s=1, marker=m, label=lab2, alpha=alp, lw = 0)
        if nrow > 2:
            dfn = df.loc[df['time']>-1]
            ax[2, typ].plot(dfn['time'], -sign*dfn['theta2'], m, markersize=1)
            ax[2, typ].plot(dfn['time'], dfn['theta1'], m, markersize=1)
            ax[2, typ].set_yticks([-pi/3, -pi/6, 0, pi/6, pi/3])
            ax[2, typ].set_yticklabels([r'$-\frac{\pi}{3}$', r'$-\frac{\pi}{6}$', r'$0$', r'$\frac{\pi}{6}$', r'$\frac{\pi}{3}$'])

    ax[0, 0].legend(loc='upper right', prop={'size': 8}, handletextpad=-0.5, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[0, 1].legend(loc='upper right', prop={'size': 8}, handletextpad=-0.5, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[1, 0].legend(loc='lower center', prop={'size': 8}, handletextpad=-0.5, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[1, 1].legend(loc='upper right', prop={'size': 8}, handletextpad=-0., borderpad=0.3, labelspacing=0, borderaxespad=0, markerscale=2.)
    ax[0,0].set_xlim(left=-start-0.1, right=0.3*start)
    for i in iax:
        i.set_xticks(())
        i.set_yticks(())
    f.suptitle('Starting at time -{}, {} convention for tip-side events'.format(start, kind))
    f.subplots_adjust(hspace=0, wspace=0);
    name='{}-{}.pdf'.format(start, kind)
    savefig('combined/'+name, bbox_inches='tight')
    print(name, 'saved')

if __name__ == "__main__":
    for i in [10, 20, 30, 50]:
        draw('mirror', i)
        draw('central', i)
