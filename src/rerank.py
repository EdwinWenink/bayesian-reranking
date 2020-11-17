'''
Bayesian Reranking 
'''

from bm25_baseline import BaselineBM25 

baseline = BaselineBM25(k=10)
baseline.rank()

topics = baseline.get_topics()
query_ids = [ str(id) for id  in topics.keys() ]
queries = [ topic['title'] for topic in topics.values()]

print(query_ids)
print(queries)


# "The events set *F* is a *sigma-algebra* of subsets of *Omega*,
# whose elements are the keyword sequences of the topics. (p.2)

# For each topic, the system outputs N retrieved passages.

