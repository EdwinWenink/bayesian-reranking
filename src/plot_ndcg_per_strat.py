import numpy as np
import matplotlib.pyplot as plt

# means @5 @10 @20
base = (0.4741, 0.4312, 0.41)
greedy = (0.4211, 0.3715, 0.3505)
top5avg = (0.4086, 0.3621, 0.3431)

# standard error @5 @10 @20
base_sem = (0.04276, 0.0381, 0.03447)
greedy_sem = (0.043, 0.03311, 0.02896)
top5avg_sem = (0.04291, 0.03353, 0.02873)

# standard deviation @5 @10 @20
base_std = (0.2993, 0.2667, 0.24)
greedy_std = (0.301, 0.2318, 0.2027)
top5avg_std = (0.3004, 0.2347, 0.2011)

def autolabel(bars, yerr):
    for i, bar in enumerate(bars):
        height = bar.get_height()
        err = yerr[i]
        ax.text(bar.get_x() + bar.get_width()/3., height+err+0.02,
                f"$\mu$={height}",
                #rotation=90,
                zorder=1,
                ha='left',
                va='top')

Nx = 3
x = np.arange(Nx)
width = 0.20

fig = plt.figure()
ax = fig.add_subplot(111)

bars1 = ax.bar(x-width, base, width, edgecolor='black', yerr=base_sem, capsize=7, hatch='/')
bars2 = ax.bar(x, greedy, width, edgecolor='black', yerr=greedy_sem, capsize=7, hatch='.')
bars3 = ax.bar(x+width, top5avg, width, edgecolor='black', yerr=top5avg_sem, capsize=7, hatch='\\')

ax.set_ylabel("nDCG")
ax.set_xlabel("Rank cut-offs")
ax.set_title("nDCG scores per rank cut-off")
ax.set_xticks(x)
ax.set_xticklabels( ('@5', '@10', '@20'))
ax.legend( (bars1, bars2, bars3), ('baseline', 'greedy', 'top 5 avg'))

autolabel(bars1, base_sem)
autolabel(bars2, greedy_sem)
autolabel(bars3, top5avg_sem)

plt.tight_layout()
# Savefig changes the ratio of the pdf, annoyingly, so better to manually safe after plot.show()
#plt.savefig('../results/eval/plot_ndcg_per_strat.pdf', format='pdf', bbox_inches='tight')
plt.show()
