import numpy as np
import matplotlib.pyplot as plt

# @5 @10 @20
base = (0.4741, 0.4312, 0.41)
greedy = (0.3932, 0.3592, 0.3396)
top5avg = (0.3835, 0.3541, 0.3367)
top10avg = (0.3812, 0.3495, 0.3341)  # currently not used

def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        print(height)
        ax.text(bar.get_x() + bar.get_width()/3., 1.05*height,
                f'{height}',
                rotation=90,
                zorder=1,
                #ha='center',
                va='bottom')

Nx = 3
x = np.arange(Nx)
width = 0.20

fig = plt.figure()
ax = fig.add_subplot(111)

bars1 = ax.bar(x-width, base, width, edgecolor='black', hatch='/')
bars2 = ax.bar(x, greedy, width, edgecolor='black', hatch='.')
bars3 = ax.bar(x+width, top5avg, width, edgecolor='black', hatch='\\')

ax.set_ylabel("nDCG")
ax.set_xlabel("Rank cut-offs")
ax.set_title("nDCG scores per rank cut-off")
ax.set_xticks(x)
ax.set_xticklabels( ('@5', '@10', '@20'))
ax.legend( (bars1, bars2, bars3), ('baseline', 'greedy', 'top 5 avg'))

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

plt.tight_layout()
plt.savefig('../results/eval/plot_ndcg_per_strat.pdf', format='pdf')
plt.show()
