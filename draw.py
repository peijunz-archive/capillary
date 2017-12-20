from capillary import edge, fitting, analyse, display
from pylab import *
from matplotlib.ticker import AutoMinorLocator
import pickle

rc('text', usetex=True)
start=30
ptsize=2
lw=0.5
df0=[analyse.analyse_raw(i) for i in range(0, 8)]
dfs=[i.loc[i['time']>-start] for i in df0]
dfs[4]['theta1']*=-1
dfs[4]['theta2']*=-1
uni=2.48
brk=-2
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
cof=180/np.pi
tt=[(3, 'oC0'), (4, 'sC1'), (5, '*C2'), (7, '>C3')]
ts=[(1, 'oC0'), (2, 'sC1'), (6, '>C3')]

def draw_old(kind='mirror'):
    cla()
    nrow = 2
    f, ax = plt.subplots(nrow, 2, sharex=True)
    #ax[0, 0].axvline(0, linestyle='-', color='#cccccc', linewidth=0.8)
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[0, 1])

    ax[1, 0].set_yticks([-60, -30, 0, 30, 60])
    ax[1, 1].set_yticks([-60, -30, 0, 30, 60])
    ax[1, 0].set_yticklabels([r'$-60^\circ$', r'$-30^\circ$', r'$0$', r'$30^\circ$', r'$60^\circ$'])
    ax[1, 1].set_yticklabels([])
    ax[0, 1].set_yticklabels([])

    ax[1, 1].get_shared_y_axes().join(ax[1, 0], ax[1, 1])

    # TIP-TIP

    cols = (r'$\textrm{tip-tip}$', r'$\textrm{tip-side}$')
    for i, col in enumerate(cols):
        ax[0, i].set_title(col, fontsize=10)
    rows = (r'$r(\mathrm{\mu m})$', r'$\theta_1, \theta_2$', r'$\theta_1, \theta_2$')[:nrow]
    for i, row in enumerate(rows):
        ax[i, 0].set_ylabel(row, fontsize=10)#, rotation=0)
    ax[1, 0].set_xlabel(r'$t(\mathrm{s})$', fontsize=10, rotation=0)
    ax[1, 1].set_xlabel(r'$t(\mathrm{s})$', fontsize=10, rotation=0)

    l=[(*i, 0) for i in tt] + [(*i, 1) for i in ts]

    iax = [f.add_axes([.379, .747, .133, .133]), 
        #f.add_axes([.545, .643, .15, .13]), 
        f.add_axes([.765, .745, .135, .135])]
    alp=1
    iax[0].set_xlabel(r'$t_c-t$', fontsize=7, labelpad=0)
    iax[0].set_ylabel(r'$r$', rotation=0, fontsize=7)#, labelpad=0)
    iax[1].set_xlabel(r'$t_c-t$', fontsize=7, labelpad=0)
    iax[1].set_ylabel(r'$r$', rotation=0, fontsize=7)#, labelpad=0)
    iax[0].set_ylim(top=900)
    iax[0].set_ylim(top=900)
    for i, m, typ in l[:1]:
        df = dfs[i]
        dfp = df.loc[df['time']<=0]

        ldf = df.loc[df['time']<brk]
        ldfp = dfp.loc[dfp['time']<brk]
        rdf = df.loc[df['time']>=brk]
        rdfp = dfp.loc[dfp['time']>=brk]

        kargs={'markersize':ptsize,
               'alpha':solid,
               'lw': lw,
               'markeredgewidth':0
               }
        ax[0, typ].plot(np.array(ldfp['time']), np.array(ldfp['rho'])*uni, m, **kargs)
        ax[0, typ].plot(rdfp['time'], rdfp['rho']*uni, m+'-', label=lab[i], **kargs)

        iax[typ].loglog(-ldfp['time'], ldfp['rho']*uni, m, **kargs)
        #iax[typ].plot(log(-ldfp['time']), log(ldfp['rho']), m, **kargs)
        iax[typ].loglog(-rdfp['time'], rdfp['rho']*uni, m+'-', **kargs)

        ax[1, typ].plot(np.array(ldf['time']), np.array(ldf['theta1'])*cof, m, **kargs)
        ax[1, typ].plot(rdf['time'], rdf['theta1']*cof, m+'-', label=r"$\theta_1\ \ $"+lab[i], **kargs)
        edge = 0.07*ptsize**2
        ms=ptsize-edge*0.5
        ax[1, typ].plot(np.array(ldf['time']), np.array(-ldf['theta2'])*cof, m, markersize=ptsize, lw =lw, markerfacecolor='none', markeredgewidth=edge, alpha=hallow)
        ax[1, typ].plot(rdf['time'], -rdf['theta2']*cof, m+'-', markersize=ms, label=r"$\theta_2\ \ $"+lab[i], lw = lw, markerfacecolor='none', markeredgewidth=edge, alpha=hallow)
    x=np.array([0.0333, 30])
    y=120*x**(1/8)*uni
    iax[0].loglog(x, y, 'k:', lw=0.4)
    iax[1].loglog(x, y, 'k:', lw=0.4)
    ax[0, 0].legend(loc='center left', prop={'size': 6}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[0, 1].legend(loc='center left', prop={'size': 6}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[1, 0].legend(loc='lower left', prop={'size': 6}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[1, 1].legend(loc='upper left', prop={'size': 6}, borderpad=0.3, labelspacing=0, markerscale=2.)
    ax[0,0].set_xlim(left=-start-0.1, right=7)
    ax[0,0].set_ylim(top=400*uni)
    iax[0].set_ylim(bottom=100)
    iax[1].set_ylim(bottom=100)
    #ax[1,0].plot(-3, 0, marker=(3, 0, 60), color='C3', markersize=15, linestyle='None', markeredgewidth=0)
    #ax[1,0].plot(-2.78, -0.29, marker=(3, 0, -110), color='C3', markersize=15, linestyle='None', markeredgewidth=0)

    #ax[1,0].plot(-3, -0.9, marker=(3, 0, 0), color='C3', markersize=15, linestyle='None', markeredgewidth=0)
    #ax[1,0].plot(-3, -1.05, marker=(3, 0, -180), color='C3', markersize=15, linestyle='None', markeredgewidth=0)

    iax[1].tick_params(labelsize=6, pad=0.3)
    iax[0].tick_params(labelsize=6, pad=0.3)
    iax[1].tick_params(labelsize=6, pad=0.3, which='minor')
    iax[0].tick_params(labelsize=6, pad=0.3, which='minor')
    #plt.setp(iax[0].get_yminorticklabels(), visible=False)
    #plt.setp(iax[1].get_yminorticklabels(), visible=False)
    #for i in iax:
        #i.set_xticks(())
        #i.set_yticks(())
    #f.suptitle('Starting at time -{}, {} convention for tip-side events'.format(start, kind))
    f.subplots_adjust(hspace=0, wspace=0);
    name='{}-{}'.format(start, kind)
    savefig('combined/'+name+'.pdf', bbox_inches='tight')
    savefig('combined/'+name+'.svg', bbox_inches='tight')
    print(name, 'saved')

def splitframe(df, brk):
    dfp = df.loc[df['time']<=0]

    ldf = df.loc[df['time']<brk]
    ldfp = dfp.loc[dfp['time']<brk]
    rdf = df.loc[df['time']>=brk]
    rdfp = dfp.loc[dfp['time']>=brk]
    return ldf, rdf, ldfp, rdfp, dfp, df

@vectorize
def Hexapole(x):
    return x**(1/8)*200
@vectorize
def Quadrupole(x):
    return x**(1/6)*200

def drawr(L, name="r"):
    clf()
    fig=gcf()
    ax=gca()
    kargs={
        'markersize':ptsize*2,
        'alpha':solid,
        'lw': lw*2,
        'markeredgewidth':0
        }
    for i, m in L:
        ldf, rdf, ldfp, rdfp, dfp, f = splitframe(df0[i], -2)
        loglog(-array(ldfp['time']), array(ldfp['rho'])*uni, m, label='', **kargs)
        ldf, rdf, ldfp, rdfp, dfp, f = splitframe(dfs[i], -2)
        loglog(-array(rdfp['time']), array(rdfp['rho'])*uni, m+'-', label=lab[i], **kargs)
    #grid(which='both')
    #grid(which='major', linewidth=0.5, linestyle=':')
    ylim(115, 1300)
    x=array([1/30, 30])
    plot(x, Hexapole(x)*1.4, '--', lw=1, label="Hexapole Interaction", color='#009900')
    plot(x, Quadrupole(x)*1.4, '-.', lw=1, label='Quadrupole Interaction', color='#000099')
    xlabel(r'$t_c-t(\mathrm{s})$')
    ylabel(r'$r(\mathrm{\mu m})$')
    legend(fontsize=8, markerscale=1.5, loc='lower right')
    plt.tick_params(axis='y', which='minor')
    yticks([200, 300, 400, 600, 1000],
           ['$200$', '$300$', '$400$', '$600$', r'$10^3$'])
    #ax.yaxis.set_minor_formatter(FormatStrFormatter('$%.0f$'))
    #ax.yaxis.set_ticklabels(['$200$', '$300$', '$400$', '', '$600$', '', '', '', ''], minor=True)
    iax=fig.add_axes([.185, .62, .26, .25])
    kargs={
        'markersize':ptsize,
        'alpha':solid,
        'lw': lw,
        'markeredgewidth':0
        }
    for i, m in L:
        ldf, rdf, ldfp, rdfp, dfp, f = splitframe(dfs[i], -2)
        iax.plot(np.array(ldfp['time']), np.array(ldfp['rho'])*uni, m, **kargs)
        iax.plot(rdfp['time'], rdfp['rho']*uni, m+'-', label=lab[i], **kargs)
    iax.set_xlabel(r'$t-t_c(\mathrm{s})$', fontsize=9, labelpad=1)
    iax.set_ylabel(r'$r(\mathrm{\mu m})$', fontsize=9, labelpad=1)
    iax.tick_params(labelsize=7, pad=1)
    savefig('combined/'+name+'-r.pdf', bbox_inches='tight')

def drawt(L, name):
    brk=-1
    clf()
    for i, m in L:
        ldf, rdf, ldfp, rdfp, dfp, df = splitframe(dfs[i], -1)
        kargs={'markersize':ptsize*1.5,
               'alpha':solid,
               'lw': lw,
               'markeredgewidth':0
               }
        plot(np.array(ldf['time']), np.array(ldf['theta1'])*cof, m, **kargs)
        plot(rdf['time'], rdf['theta1']*cof, m+'-', label=r"$\theta_1\ \ $"+lab[i], **kargs)
        edge = 0.14*ptsize
        ms=ptsize*1.5-edge*0.5
        plot(np.array(ldf['time']), np.array(-ldf['theta2'])*cof, m, markersize=ms, lw =lw, markerfacecolor='none', markeredgewidth=edge, alpha=hallow)
        plot(rdf['time'], -rdf['theta2']*cof, m+'-', markersize=ms, label=r"$\theta_2\ \ $"+lab[i], lw = lw, markerfacecolor='none', markeredgewidth=edge, alpha=hallow)
    xlim(right=5)
    #k=max(64, ylim()[1])
    #print(k)
    #ylim(top=k)
    ylim(-75,64)
    grid(which='both', linewidth=0.5, linestyle=':')
    yticks([-60, -30, 0, 30, 60])
    if len(L)==3:
        k='upper'
    else:
        k='lower'
    legend(fontsize=8, loc=k+' left', markerscale=2.)
    xlabel(r'$t(s)$')
    ylabel(r'$\theta_1, \theta_2(\mathrm{deg})$')
    savefig('combined/'+name+'-theta.svg', bbox_inches='tight')
    savefig('combined/'+name+'-theta.pdf', bbox_inches='tight')

if __name__ == "__main__":
    tt=[(3, 'oC0'), (4, 'sC1'), (5, '*C2'), (7, '>C3')]
    ts=[(1, 'oC0'), (2, 'sC1'), (6, '>C3')]
    drawr(tt, 'tip-tip')
    drawr(ts, 'tip-side')
    #drawt(tt, 'tip-tip')
    #drawt(ts, 'tip-side')
