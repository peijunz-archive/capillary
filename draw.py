from capillary import edge, fitting, analyse, display
from pylab import *
from matplotlib.ticker import AutoMinorLocator
import pickle

rc('text', usetex=True)
start=30
ptsize=2
lw=0.3
try:
    pickle.load(open('30seconds.pkl', 'r'))
except:
    df0=[analyse.analyse_raw(i) for i in range(0, 8)]
    dfs=[i.loc[i['time']>-start] for i in df0]
    #pickle.dump(dfs, open('30seconds.pkl', 'w'))

brk=-1
# Three subplots sharing both x/y axes
solid=0.7
hallow=0.7
lab=('',
     r'$T/L=1/25\mathrm{, trial\ 1}$',
     r'$T/L=1/25\mathrm{, trial\ 2}$',
     r'$T/L=1/25\mathrm{, trial\ 1}$',
     r'$T/L=1/25\mathrm{, trial\ 2}$',
     r'$T/L=1/25\mathrm{, trial\ 3}$',
     r'$T/L=1/50$',
     r'$T/L=1/50$')
def draw(kind='mirror', ):
    cla()
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
    rows = (r'$r/\mathrm{px}$', r'$\theta_1, \theta_2/\mathrm{rad}$', r'$\theta_1, \theta_2$')[:nrow]
    for i, row in enumerate(rows):
        ax[i, 0].set_ylabel(row, fontsize=10)#, rotation=0)
    ax[1, 0].set_xlabel(r'$t/\mathrm{s}$', fontsize=10, rotation=0)
    ax[1, 1].set_xlabel(r'$t/\mathrm{s}$', fontsize=10, rotation=0)

    tt=[(3, 'oC0'), (4, 'sC1'), (5, '>C2'), (7, '*C3')]
    ts=[(1, 'oC0'), (2, 'sC1'), (6, '>C2')]

    l=[(*i, 0) for i in tt] + [(*i, 1) for i in ts]

    iax = [f.add_axes([.382, .75, .13, .13]), 
        #f.add_axes([.545, .643, .15, .13]), 
        f.add_axes([.77, .75, .13, .13])]
    alp=1
    for i, m, typ in l:
        df = dfs[i]
        dfp = df.loc[df['time']<0]

        ldf = df.loc[df['time']<brk]
        ldfp = dfp.loc[dfp['time']<brk]
        rdf = df.loc[df['time']>=brk]
        rdfp = dfp.loc[dfp['time']>=brk]

        kargs={'markersize':ptsize,
               'alpha':solid,
               'lw': lw,
               'markeredgewidth':0
               }
        ax[0, typ].plot(np.array(ldfp['time']), np.array(ldfp['rho']), m, **kargs)
        ax[0, typ].plot(rdfp['time'], rdfp['rho'], m+'-', label='$r\ \ $'+lab[i], **kargs)

        iax[typ].loglog(-ldfp['time'], ldfp['rho'], m, **kargs)
        #iax[typ].plot(log(-ldfp['time']), log(ldfp['rho']), m, **kargs)
        iax[typ].loglog(-rdfp['time'], rdfp['rho'], m+'-', **kargs)

        ax[1, typ].plot(np.array(ldf['time']), np.array(ldf['theta1']), m, **kargs)
        ax[1, typ].plot(rdf['time'], rdf['theta1'], m+'-', label=r"$\theta_1\ \ $"+lab[i], **kargs)
        edge = 0.07*ptsize**2
        ms=ptsize-edge*0.5
        ax[1, typ].plot(np.array(ldf['time']), np.array(-ldf['theta2']), m, markersize=ptsize, lw =lw, markerfacecolor='none', markeredgewidth=edge, alpha=hallow)
        ax[1, typ].plot(rdf['time'], -rdf['theta2'], m+'-', markersize=ms, label=r"$\theta_2\ \ $"+lab[i], lw = lw, markerfacecolor='none', markeredgewidth=edge, alpha=hallow)
    x=np.array([0.0333, 30])
    y=120*x**(1/8)
    iax[0].loglog(x, y, 'k:', lw=0.4)
    iax[1].loglog(x, y, 'k:', lw=0.4)
    ax[0, 0].legend(loc='center left', prop={'size': 7}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[0, 1].legend(loc='center left', prop={'size': 7}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[1, 0].legend(loc='lower left', prop={'size': 7}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[1, 1].legend(loc='upper left', prop={'size': 7}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[0,0].set_xlim(left=-start-0.1)
    ax[0,0].set_ylim(top=400)
    ax[1,0].plot(-3, 0, marker=(3, 0, 60), color='C3', markersize=15, linestyle='None', markeredgewidth=0)
    ax[1,0].plot(-2.78, -0.29, marker=(3, 0, -110), color='C3', markersize=15, linestyle='None', markeredgewidth=0)

    ax[1,0].plot(-3, -0.9, marker=(3, 0, 0), color='C3', markersize=15, linestyle='None', markeredgewidth=0)
    ax[1,0].plot(-3, -1.05, marker=(3, 0, -180), color='C3', markersize=15, linestyle='None', markeredgewidth=0)

    #iax[0].minorticks_off()
    iax[1].tick_params(labelsize=6, pad=0.3)
    iax[0].tick_params(labelsize=6, pad=0.3)
    plt.setp(iax[0].get_yminorticklabels(), visible=False)
    plt.setp(iax[1].get_yminorticklabels(), visible=False)
    #for i in iax:
        #i.set_xticks(())
        #i.set_yticks(())
    #f.suptitle('Starting at time -{}, {} convention for tip-side events'.format(start, kind))
    f.subplots_adjust(hspace=0, wspace=0);
    name='{}-{}'.format(start, kind)
    savefig('combined/'+name+'.pdf', bbox_inches='tight')
    savefig('combined/'+name+'.svg', bbox_inches='tight')
    print(name, 'saved')

if __name__ == "__main__":
    draw()
