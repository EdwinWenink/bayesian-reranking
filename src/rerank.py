'''
Bayesian Reranking 
'''

from bm25_baseline import BaselineBM25 
from pyserini.index import IndexReader
from collections import defaultdict
from operator import itemgetter
import numpy as np
#import gensim
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

import itertools

class Bayesian_Reranker():
    
    def __init__(self, seed=0, max_iter=1000):
        self.seed = seed
        self.max_iter = max_iter

        # TODO ideally we don't want to first rank every time for the reranking 
        # Either integrate the reranking in the original ranking; or load a pre-existing ranking 
        self.baseline = BaselineBM25(k=100)
        self.baseline.rank()

        # For each topic, the system outputs N retrieved articles.
        self.batch_hits = self.baseline.get_batch_hits()

        # Read index to retrieve document contents
        # N.B. the `contents` field is currently empty; we stored "raw" instead.
        self.index_loc = self.baseline.get_index_loc()
        reader = IndexReader(self.index_loc)

        # Vocabulary in index
        #vocabulary = [ term.term for term in reader.terms()]
        #print(f"{len(vocabulary)} terms in vocabulary")

        # Topics and the retrieved articles are represented as the keyword sequences
        self.topics = self.baseline.get_topics()
        self.topic_keywords = { id: topic['title'].lower().split() for (id, topic) in self.topics.items() } 
        self.query_ids = self.baseline.get_query_ids()

        # Next line returns preprocessed documents per query 
        # TODO; this takes RAW terms, including metadata etc., which may not be ideal
        # I'd prefer to only have the contents, but `contents` property is not currently available in our index
        docs_per_query = { query_id: [ reader.analyze( reader.doc(hit.docid).raw()) for hit in hits] for query_id, hits in self.batch_hits.items() }

        # Prepare bag-of-words dataset for gensim
        self.X = defaultdict(list)
        for id in self.query_ids:
            dictionary = Dictionary(docs_per_query[id])
            # Dictionary expects a list of lists, elements being lists of tokens
            self.X[id] = [dictionary.doc2bow(doc) for doc in docs_per_query[id]]

    def docs_to_topic(self, X):
        """ 
        Iteratively assigns documents to a topic
        until topic distribution does no longer change
        """

        def step(k, alpha):
            lda = LdaModel(corpus=X, num_topics=k, alpha=alpha, random_state=self.seed)
            preds = lda[X]
            argmax = [ max(topics, key=itemgetter(1))[0] for topics in preds]
            topics, topic_counts = np.unique(argmax, return_counts=True)
            return topics, topic_counts, argmax

        # Initialisation
        k = len(X)  # init: k=N (=1000)
        prev = np.zeros(k)
        i = 1

        # Find starting topics
        print(f"Iteration {i}: running with k={k}")
        # Initial run with a symmetric alpha prior
        lda = LdaModel(corpus=X, num_topics = k, alpha='symmetric', random_state=self.seed)
        preds = lda[X]
        argmax = [ max(topics, key=itemgetter(1))[0] for topics in preds]
        topics, topic_counts = np.unique(argmax, return_counts=True)

        # Convergence criterion is only a heuristic w.r.t. the paper
        # Checks topic counts instead of ensuring all document per topic stay the same 
        while not np.array_equal(prev, topic_counts) and i < self.max_iter:
            i += 1
            prev = topic_counts
            k = len(topics)  
            print(f"Iteration {i}: running with k={k}")
            # pass topic distribution of previous iteration as alpha prior
            topics, topic_counts, argmax = step(k, topic_counts/len(X))

        if i == self.max_iter:
            print(f"Maximum iterations reached. Terminated with {len(topics)} topics ")
        else:
            print(f"Converged. {len(topics)} topics.")
        print(f"Topic counts: {topic_counts}")
        print(f"Topic assignments: {argmax}")

        # Create a dictionary with docs per topic
        docs_per_topic  = defaultdict(list)
        for topic_id in topics:
            docs_per_topic[ topic_id ].append(np.where(argmax == topic_id))
        return docs_per_topic

    def weigh_topics(self, scores):
        pass

    def picking_strategy(self):
        pass

    def rerank(self):
        # Try for the first topic only

        # Original document ids and scores
        doc_ids = self.baseline.get_doc_ids()
        scores = self.baseline.get_scores()

        for id in self.query_ids:
            print(f"Reranking for topic {id}")
            docs_per_topic = self.docs_to_topic(self.X[id])
            print(docs_per_topic)
            # TODO we need access to the original docids here; 
            print(doc_ids[id])
            print(scores[id])
            # TODO the actual reranking here within the loop
            # weigh_topics(scores)
            # picking_strategy()


if __name__ == "__main__":
    reranker = Bayesian_Reranker()
    reranker.rerank()
