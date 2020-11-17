'''
Bayesian Reranking 
'''

from bm25_baseline import BaselineBM25 
from pyserini.index import IndexReader

class Bayesian_Reranker():
    
    def __init__(self):
        # 10 just for quick testing; should be 1000
        self.baseline = BaselineBM25(k=10)
        self.baseline.rank()

        # For each topic, the system outputs N retrieved passages.
        self.batch_hits = self.baseline.get_batch_hits()

        # Topics and the retrieved passages are represented as the keyword sequences
        self.topics = self.baseline.get_topics()
        # TODO vervangen met nltk tokenizer? Overal gelijktrekken
        self.topic_keywords = { id: topic['title'].lower().split() for (id, topic) in self.topics.items() } 
        print(self.topic_keywords)

        # Read index to retrieve document contents
        index_loc = self.baseline.get_index_loc()
        reader = IndexReader(index_loc)

        # get document vectors
        # vereist docids: cf. hits[i].docid
        #doc_vector = reader.get_document_vector(id)

    def rerank(self):
        pass


if __name__ == "__main__":
    reranker = Bayesian_Reranker()

#query_ids = sorted([ str(id) for id  in topics.keys() ])
#queries = [ topic['title'] for topic in topics.values()]
#print(query_ids)
