'''
Bayesian Reranking 
'''

from bm25_baseline import BaselineBM25 
from pyserini.index import IndexReader
from collections import defaultdict
from operator import itemgetter
import numpy as np
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from utils import Utils
import itertools
from functools import partial


class Bayesian_Reranker():
    
    def __init__(self, seed=0, max_iter=1000):
        self.seed = seed
        self.max_iter = max_iter
        self.utils = Utils()

        # TODO ideally we don't want to first rank every time for the reranking 
        # Either integrate the reranking in the original ranking; or load a pre-existing ranking 
        self.baseline = BaselineBM25(k=20)
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
        docs_per_topic  = defaultdict(partial(np.ndarray, 0))
        for topic_id in topics:
            docs_per_topic[ topic_id ] = np.where(argmax == topic_id)[0]
        return docs_per_topic

        """
        defaultdict(<class 'list'>, {
            0: [(array([ 0,  1,  6, 13, 15, 16, 17, 18], dtype=int64),)],
            1: [(array([ 3,  5,  7, 10, 11, 12, 14, 19], dtype=int64),)],
            2: [(array([4, 8, 9], dtype=int64),)], 
            3: [(array([2], dtype=int64),)]})
        """
    #helper functions
    
    #finds longest list
    def find_max_list(self, lst):
        list_len = [len(i) for i in lst]
        return max(list_len)
    
    #helps to merge lists in alternating fashion
    #subtopic_lists is a list of lists and each item is a subtopic_list
    def merger(self, subtopic_lists, merge_list):
        for x in range(len(subtopic_lists)):
            try:
                merge_list.append(subtopic_lists[x].pop(0))
            except IndexError:
                continue
       
        return merge_list

    def weigh_topics(self, docs_per_topic_dict, doc_scores, doc_ids):
        avg_scores_and_ids = []
        highest_scores_and_ids = []

        #calculate weighted average of each subtopic based on first k results of subtopic
        avg_based_on_first_k = 3

        #loop over dictionairy, so for each subtopic
        for key in docs_per_topic_dict:
            docs_topic_sub = docs_per_topic_dict[key]
            #print(docs_topic_sub)
            doc_scores_sub = []
            doc_ids_sub = []
            for x in docs_topic_sub:
            #for x in np.nditer(a):
                doc_scores_sub.append(doc_scores[x])
                doc_ids_sub.append(doc_ids[x])
            
            #deze twee lijsten zijn nodig voor de 2 verschillende rankingen
            #om te sorteren op weighted average of first k
            avg_scores_and_ids.append((sum(doc_scores_sub[:avg_based_on_first_k])/len(doc_scores_sub[:avg_based_on_first_k]), doc_ids_sub, doc_scores_sub))
            #greedy
            highest_scores_and_ids.append(((doc_scores_sub[0]), (doc_ids_sub), doc_scores_sub))    

        #hier kan je dus ook kiezen en switchen of je op gemiddelde score of hoogste 1e score wil ranken
        #sorted based on first element of tuple
        return sorted(avg_scores_and_ids,key=itemgetter(0), reverse=True)
        #return sorted(highest_scores_and_ids,key=itemgetter(0), reverse=True)

    def reranking_merge(self, weighted_tuple_lst):
        final_list_ids = []
        final_list_scores = []
        ordered_topic_ids = []
        ordered_topic_scores = []


        #pak alleen doc_id element, drop scores/weighted avg
        for tpl in weighted_tuple_lst:
            ordered_topic_ids.append(tpl[1])
            ordered_topic_scores.append(tpl[2])
        
        #we need to do the merger as many times as the length of the longest list
        iters_needed = self.find_max_list(ordered_topic_ids)

        #merge lists in ordered_topic_ids in alternating fashion
        for i in range(iters_needed):
            final_list_ids = self.merger(ordered_topic_ids, final_list_ids)
            final_list_scores = self.merger(ordered_topic_scores, final_list_scores)
        
        return final_list_ids, final_list_scores


    def picking_strategy(self):
        pass

    def rerank(self):
        # Original document ids and scores
        doc_ids = self.baseline.get_doc_ids()
        scores = self.baseline.get_scores()
        reranked_doc_ids = defaultdict(partial(np.ndarray, 0)) 
        reranked_doc_scores = defaultdict(partial(np.ndarray, 0)) 

        # TODO pick different strategies
        strategy= "TOP-K-AVG"

        for id in self.query_ids:
            print(f"Reranking for topic {id}")
            docs_per_topic = self.docs_to_topic(self.X[id])
            reranked_ids, reranked_scores = self.reranking_merge(self.weigh_topics(docs_per_topic, scores[id], doc_ids[id]))
            #rankings naar dictionairy
            reranked_doc_ids[id] = reranked_ids
            reranked_doc_scores[id] = reranked_scores

        # Write rankings to file 
        run_name = f"RERANK-{strategy}"
        self.utils.write_rankings(self.query_ids, reranked_doc_ids, reranked_doc_scores, run_name)

if __name__ == "__main__":
    reranker = Bayesian_Reranker()
    reranker.rerank()
