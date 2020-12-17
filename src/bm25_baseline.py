"""
This file produces baseline results using Anserini's BM25 implementation
on the WashingtonPost corpus, using Common Core 2018 topics
"""

import os
import pyserini
from utils import Utils
from pyserini.search import SimpleSearcher, get_topics

class BaselineBM25():

    def __init__(self, k, index_loc =  '../../anserini/indexes/lucene-wapost.v2.pos+docvectors+raw'):
        self.utils = Utils()
        # Make sure you have produced this lucene index before
        self.index_loc = index_loc
        self.searcher = SimpleSearcher(self.index_loc)
        self.k = k  # number of hits to return 
        self.searcher.set_bm25(k1=0.9, b=0.4)  # BM25 params
        #searcher.set_rm3(10, 10, 0.5)  # relevance feedback
        self.batch_hits = {}
        self.topics = get_topics('core18')
        self.query_ids = [ str(id) for id  in self.topics.keys() ]
        self.queries = [ topic['title'] for topic in self.topics.values()]
        self.doc_ids = {}
        self.scores = {}

    def rank(self):
        print("Ranking for all topics in progress ...")
        # Perform batch search on all queries
        # hits contains: docid, retrieval score, and document content
        self.batch_hits = self.searcher.batch_search(self.queries, self.query_ids, k = self.k)

        # Inspect results for first query
        #print("Scores for first query:")
        #self.utils.print_top_n_results(self.batch_hits[self.query_ids[0]], 10)

        # Produce a file suitable to be used with trec-eval
        self.doc_ids = { query_id: [ hit.docid for hit in hits] for query_id, hits in self.batch_hits.items() }
        self.scores = { query_id: [ hit.score for hit in hits] for query_id, hits in self.batch_hits.items() }
        run_name = f"BASELINE-N{self.k}"
        self.utils.write_rankings(self.query_ids, self.doc_ids, self.scores, run_name)

    def get_topics(self):
        return self.topics

    def get_batch_hits(self):
        return self.batch_hits

    def get_index_loc(self):
        return self.index_loc

    def get_query_ids(self):
        return self.query_ids

    def get_queries(self):
        return self.queries

    def get_doc_ids(self):
        return self.doc_ids

    def get_scores(self):
        return self.scores

if __name__ == "__main__":
    index_loc = '../../anserini/indexes/lucene-wapost.v2.pos+docvectors+contents'
    bm25 = BaselineBM25(k=1000, index_loc=index_loc)
    bm25.rank()
