#!/bin/bash

METRICS=('ndcg' 'ndcg_cut.5' 'ndcg_cut.10' 'ndcg_cut.20')
N='N100'
STRATS=('GREEDY' 'TOP-5-AVG' 'TOP-10-AVG')

for METRIC in "${METRICS[@]}"
do
    for STRAT in "${STRATS[@]}"
    do
        echo $METRIC $STRAT
        python compare_runs_fork.py --metric $METRIC --qrels ../results/qrels.core18.txt --base ../results/results-BASELINE-$N.txt --comparison ../results/results-RERANK-$N-$STRAT.txt --N $N --strategy $STRAT
    done
done
