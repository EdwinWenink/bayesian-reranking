import os
import pyserini
from utils import *

# --------------
# SimpleSearcher
# --------------

# For ref, see here: https://github.com/castorini/pyserini/blob/master/pyserini/search/_searcher.py
# also see the bulk search option
from pyserini.search import SimpleSearcher

# Make sure you have produced this lucene index
index_loc = '../../anserini/indexes/lucene-wapost.v2.pos+docvectors+raw'
searcher = SimpleSearcher(index_loc)

# Configure search options and repeat the same query
searcher.set_bm25(0.9, 0.4)  # BM25 params
#searcher.set_rm3(10, 10, 0.5)  # relevance feedback

# hits contains: docid, retrieval score, and document content
# N.B. "black bear attacks" is the title of topic 336
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

# See class Document in https://github.com/castorini/pyserini/blob/master/pyserini/search/_base.py
# properties: docid; id (alias); lucene_document; contents; raw
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
from pyserini.search import get_topics
topics = get_topics('core18')

# Get some information on all topics
print_topic(topics)

# More detailed info on the black bear example
print_topic(topics, id=336)

# ----------------
# Evaluation
# ----------------

# Use trec_eval for evaluation

# ----------------
# Reranking
# ----------------

# Found this: https://github.com/castorini/pyserini/blob/master/pyserini/search/reranker.py

