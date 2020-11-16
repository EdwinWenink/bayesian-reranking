import os
import pyserini


def print_top_n_results(hits, n):
    for i in range(0, n):
        print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')


def top_n_words(doc_vector, n=10):
    # Values of doc vector can include None, which blocks comparison
    for i, (k, v) in enumerate(sorted(doc_vector.items(), key=lambda x: (x[1] is not None, x[1]), reverse=True)):
        print(f"{i+1}. {k}:{v}")
        if i==n: break


# --------------
# SimpleSearcher
# --------------

# For ref, see here: https://github.com/castorini/pyserini/blob/master/pyserini/search/_searcher.py

from pyserini.search import SimpleSearcher
index_loc = '../../anserini/indexes/lucene-wapost.v2.pos+docvectors+raw'
searcher = SimpleSearcher(index_loc)

# Configure search options and repeat the same query
searcher.set_bm25(0.9, 0.4)  # BM25 params
#searcher.set_rm3(10, 10, 0.5)  # relevance feedback

# hits contains: docid, retrieval score, and document content
hits = searcher.search('black bear attacks')

# Print first 10 hits
print_top_n_results(hits, 10)

# ----------------
# IndexReaderUtils
# ----------------

from pyserini.index import IndexReader

# Now we do not search the index, but retrieve a document directly from the index
reader = IndexReader(index_loc)

# Retrieve a document using its docid
#id = 'd6ed7028c686e5756ceb0aa0c9b62e0d'
id = hits[0].docid
doc = reader.doc(id).raw()
#print(doc)

# Get analyzed form (tokenized, stemmed, stopwords removed)
analyzed = reader.analyze(doc)
#print(analyzed)

# Raw document VECTOR is also stored
doc_vector = reader.get_document_vector(id)
top_n_words(doc_vector, 10)

# ----------------
# Topics and Qrels 
# ----------------

# Things to look at from other demo's

## Get TOPICS (cf. TREC parlance)
#from pyserini.search import get_topics
#topics = get_topics('msmarco_passage_dev_subset')
#print(f'{len(topics)} queries total')

# ----------------
# Evaluation
# ----------------

# Use trec_eval for evaluation

# ----------------
# Reranking
# ----------------

# Found this: https://github.com/castorini/pyserini/blob/master/pyserini/search/reranker.py

