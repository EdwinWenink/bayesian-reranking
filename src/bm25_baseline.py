"""
This file produces baseline results using Anserini's bm25 implementation
on the WashingtonPost corpus, using Common Core 2018 topics
"""

import os
import pyserini
from utils import Utils
from pyserini.search import SimpleSearcher, get_topics

utils = Utils()

# Make sure you have produced this lucene index
index_loc = '../../anserini/indexes/lucene-wapost.v2.pos+docvectors+raw'
searcher = SimpleSearcher(index_loc)

# Configure search options and repeat the same query
searcher.set_bm25(0.9, 0.4)  # BM25 params
#searcher.set_rm3(10, 10, 0.5)  # relevance feedback

topics = get_topics('core18')
query_ids = [ str(id) for id  in topics.keys() ]
queries = [ topic['title'] for topic in topics.values()]

# Perform batch search on all queries
# TODO what should this be?
# I think baseline regressions use *all* results
k = 1000  # number of hits to return 
# hits contains: docid, retrieval score, and document content
batch_hits = searcher.batch_search(queries, query_ids, k = k)

# Inspect results for first query
print("Scores for first query:")
utils.print_top_n_results(batch_hits[query_ids[0]], 10)

# Produce a file suitable to be used with trec-eval

# Following two lines produce flattened lists, which is not handy
#doc_ids = [ hit.docid for hits in batch_hits.values() for hit in hits ]
#scores = [ hit.score for hits in batch_hits.values() for hit in hits ]

# Have query results in a sub-list
doc_ids = [ [ hit.docid for hit in hits] for hits in batch_hits.values() ]
scores = [ [ hit.score for hit in hits] for hits in batch_hits.values() ]

run_name = "BASELINE"
utils.write_rankings(query_ids, doc_ids, scores, run_name)
