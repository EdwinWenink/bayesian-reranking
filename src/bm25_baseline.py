"""
This file produces baseline results using Anserini's BM25 implementation
on the WashingtonPost corpus, using Common Core 2018 topics
"""

import os
import pyserini
from utils import Utils
from pyserini.search import SimpleSearcher, get_topics

class BaselineBM25():

    def __init__(self, k):
        self.utils = Utils()
        # Make sure you have produced this lucene index before
        self.index_loc = '../../anserini/indexes/lucene-wapost.v2.pos+docvectors+raw'
        self.searcher = SimpleSearcher(self.index_loc)
        self.k = k  # number of hits to return 
        self.searcher.set_bm25(k1=0.9, b=0.4)  # BM25 params
        #searcher.set_rm3(10, 10, 0.5)  # relevance feedback
        self.batch_hits = {}
        self.topics = get_topics('core18')

    def rank(self):
        # Perform batch search on all queries
        # hits contains: docid, retrieval score, and document content
        query_ids = [ str(id) for id  in self.topics.keys() ]
        queries = [ topic['title'] for topic in self.topics.values()]
        self.batch_hits = self.searcher.batch_search(queries, query_ids, k = self.k)

        # Inspect results for first query
        print("Scores for first query:")
        self.utils.print_top_n_results(self.batch_hits[query_ids[0]], 10)

        # Produce a file suitable to be used with trec-eval
        doc_ids = { query_id: [ hit.docid for hit in hits] for query_id, hits in self.batch_hits.items() }
        scores = { query_id: [ hit.score for hit in hits] for query_id, hits in self.batch_hits.items() }
        run_name = "BASELINE"
        self.utils.write_rankings(query_ids, doc_ids, scores, run_name)

    def get_topics(self):
        return self.topics

    def get_batch_hits(self):
        return self.batch_hits()

if __name__ == "__main__":
    bm25 = BaselineBM25(k=1000)
    bm25.rank()
