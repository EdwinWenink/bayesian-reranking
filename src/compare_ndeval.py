"""
Script that evaluates csv output from TREC ndeval script;
this is another output format than from trec_eval

Intended to have the same functionality as the anserini 'compare_runs.py' script
(and a bit more)
"""

import os
import numpy as np
import scipy.stats
import statistics
import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
from pathlib import Path

# Example names:
#ndeval-N100-GREEDY-alpha{0, 05 1}.csv
#ndeval-N100-BASELINE-alpha{0, 05 1}.csv


def t_test(base, comp):
    '''
    Expects two lists of paired scores belonging to the same run settings
    '''
    (stat, p) = scipy.stats.ttest_rel(base, comp)
    return stat, p

def compare(base_dfs, metrics, alphas):
    for metric in metrics:
        base_avg_per_alpha = []
        comp_avg_per_alpha = []
        for alpha in alphas:
            topics = base_dfs[alpha]['topic']
            base = base_dfs[alpha][metric]
            comp = comp_dfs[alpha][metric]
            n_topics = len(base)-1  # 50 excluding row with averages

            '''
            This part is almost verbatim cf. compare_runs.py in anserini
            '''
            all_results = []
            num_better = 0
            num_worse = 0
            num_unchanged = 0
            biggest_gain = 0
            biggest_gain_topic = ''
            biggest_loss = 0
            biggest_loss_topic = ''

            for i in range(n_topics):
                base_score = base[i]
                comp_score = comp[i]
                diff = comp_score - base_score
                key = topics[i]

                if diff > 0.01:
                    num_better += 1
                elif diff < -0.01:
                    num_worse += 1
                else:
                    num_unchanged += 1
                if diff > biggest_gain:
                    biggest_gain = diff
                    biggest_gain_topic = key
                if diff < biggest_loss:
                    biggest_loss = diff
                    biggest_loss_topic = key
                all_results.append((key, diff))
                print(f'{key}\t{base_score:.4}\t{comp_score:.4}\t{diff:.4}')

            print(f'METRIC {metric}, ALPHA {alpha}')
            print('-'*40)
            print(f'base mean: {np.mean(base):.4}')
            print(f'comp mean: {np.mean(comp):.4}')
            print(f'better (diff > 0.01): {num_better:>3}')
            print(f'worse  (diff > 0.01): {num_worse:>3}')
            print(f'(mostly) unchanged  : {num_unchanged:>3}')
            print(f'biggest gain: {biggest_gain:.4} (topic {biggest_gain_topic})')
            print(f'biggest loss: {biggest_loss:.4} (topic {biggest_loss_topic})')
            stats = t_test(base, comp) # stat, p 
            print(f'T-statistic: {stats[0]:.6}, p-value: {stats[1]:.6}')
            plot_diff_per_query(all_results, alpha, metric, stats)

            base_avg_per_alpha.append(base[n_topics])
            comp_avg_per_alpha.append(comp[n_topics])

        # Plot average scores per alpha for metric 
        plot_avg_per_alpha(base_avg_per_alpha, comp_avg_per_alpha, metric, alphas)


def plot_avg_per_alpha(base_avgs, comp_avgs, metric, alphas, output_path="../results/ndeval/"):
    plt.figure()
    plt.title(f"Scores for {metric}")
    plt.ylabel("Mean $\\alpha$-nDCG over all topics ")
    plt.xlabel("$\\alpha$")
    plt.scatter(alphas, base_avgs, zorder=1, label="Baseline")
    plt.plot(alphas, base_avgs, alpha=0.6)
    plt.scatter(alphas, comp_avgs, label="Reranking")
    plt.plot(alphas, comp_avgs, zorder=1, alpha=0.6)
    plt.legend()
    output_fn = os.path.join(output_path, f'{metric}_per_alpha.pdf')
    Path(output_path).mkdir(parents=True, exist_ok=True)
    plt.savefig(output_fn, bbox_inches='tight', format='pdf')


def plot_diff_per_query(all_results, alpha, metric, stats, ymin=-1, ymax=1, output_path="../results/ndeval/"):
    """
    only minor adjustments w.r.t. 'compare_runs.py'
    """
    fig, ax = plt.subplots(1, 1, figsize=(16, 3))  # TODO misschien aanpassen als dit niet in ons report past
    all_results.sort(key = itemgetter(1), reverse=True)
    x = [_x+0.5 for _x in range(len(all_results))]
    y = [float(ele[1]) for ele in all_results]
    ax.bar(x, y, width=0.6, align='edge')
    ax.set_xticks(x)
    ax.set_xticklabels([int(ele[0]) for ele in all_results], {'fontsize': 8}, rotation='vertical')
    ax.grid(True)
    ax.set_title(f"Per-topic analysis on {metric} with $\\alpha$={alpha:.2} (t={stats[0]:.6}, p={stats[1]:.6}) ")
    ax.set_xlabel('Topics')
    ax.set_ylabel('Difference w.r.t baseline')
    ax.set_ylim(ymin, ymax)
    output_fn = os.path.join(output_path, 'per_query_{}_a_{}.pdf'.format(metric, alpha))
    Path(output_path).mkdir(parents=True, exist_ok=True)
    plt.savefig(output_fn, bbox_inches='tight', format='pdf')


if __name__ == '__main__':

    # Select measures of interest; we care about alpha-nDCG
    metrics = ['alpha-nDCG@5', 'alpha-nDCG@10', 'alpha-nDCG@20']
    cols = ['topic'] + metrics
    alphas = ['0', '05', '1']
    run_names = []
    comp_dfs = {}
    base_dfs = {}

    for alpha in alphas:
        base = pd.read_csv(f'../results/eval/ndeval-N100-BASELINE-alpha{alpha}.csv', sep=',', header=0)
        comp = pd.read_csv(f'../results/eval/ndeval-N100-GREEDY-alpha{alpha}.csv', sep=',', header=0)
        run_names.append(comp.iloc[0][0])
        # Only keep metrics of interest
        comp_dfs[alpha] = comp[cols]
        base_dfs[alpha] = base[cols]

    compare(base_dfs, metrics, alphas)
