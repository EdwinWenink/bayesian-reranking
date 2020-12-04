'''
Reranking with Latent Dirichlet Analysis
----------------------------------------
This script does not contain the actual reranking 
but is a playground for the Bayesian procedure until convergence
''' 

from collections import defaultdict
from operator import itemgetter
import numpy as np
#import gensim
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

# Delete later
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import make_multilabel_classification


def docs_to_topic(X):
    """ 
    Iteratively assigns documents to a topic
    until topic distribution does no longer changeo

    TODO: Update priors along the way

    doc_topic_prior_float:
    Prior of document topic distribution theta. If the value is None, it is 1 / n_components.

    topic_word_prior_float:
    Prior of topic word distribution beta. If the value is None, it is 1 / n_components.
    """

#---------------------------
    def step(k):
        # TODO prior
        #lda = LdaModel(corpus=X, num_topics = k, alpha=prior, random_state=0)
        lda = LdaModel(corpus=X, num_topics = k, random_state=0)
        preds = lda[X]
        argmax = [ max(topics, key=itemgetter(1))[0] for topics in preds]
        topics, topic_counts = np.unique(argmax, return_counts=True)
        return topics, topic_counts, argmax

    k = len(X)  # init: k=N
    prev = np.zeros(k)
    i = 1

    # Find starting topics
    print(f"Iteration {i}: running with k={k}")
    # first run with a symmetric alpha prior
    lda = LdaModel(corpus=X, num_topics = k, alpha='symmetric', random_state=0)
    preds = lda[X]
    argmax = [ max(topics, key=itemgetter(1))[0] for topics in preds]
    topics, topic_counts = np.unique(argmax, return_counts=True)

    # Convergence criterium is only a heuristic w.r.t. the paper
    # Checks topic counts instead of ensuring all document per topic stay the same 
    while not np.array_equal(prev, topic_counts):
        i += 1
        prev = topic_counts
        k = len(topics)  
        print(f"Iteration {i}: running with k={k}")
        topics, topic_counts, argmax = step(k)

    print(f"Converged. {len(topics)} topics.")
    print(f"Topic counts: {topic_counts}")
    print(f"Topic assignments: {argmax}")

    docs_per_topic  = defaultdict(list)

    # Create a dictionary with docs per topic
    for topic_id in topics:
        # Uncommented following line if you want to return actual docs
        #docs_per_topic[ topic_id ].append(X[np.where(argmax == topic_id)])
        docs_per_topic[ topic_id ].append(np.where(argmax == topic_id))
    return docs_per_topic


# Initialization of term dictionary; in this case for 9 2 a 3-word documents
print(common_texts)
common_dictionary = Dictionary(common_texts)
print(common_dictionary)  # prints 12 unique tokens
print(common_dictionary.keys())  # prints 12 unique tokens

# Create a corpus from a list of texts
# BoW: Bag-of-Words representation for each document: (token_id[int], token_count[float]) tuples
X = [common_dictionary.doc2bow(text) for text in common_texts]
print("X: ", X)
# X can also be a sparse matrix with (n_docs, n_terms); that may be handier

lda = LdaModel(corpus=X, num_topics = 10, alpha='symmetric')

# Full document-term matrix
print(lda.get_topics())

# TODO figure out how to use LdaState; need to initialize it first I guess
# Get posterior probabilities over topics
#print(lda.LdaState().get_lambda())
# Get log posterior probabilities for each topic
#print(lda.LdaState().get_Elogbeta())

docs_per_topic = docs_to_topic(X)
print(docs_per_topic)

# After this step, we need to order the topics on importance to determine picking order for reranking

def visualize():
    # just for later
    import pyLDAvis
    import pyLDAvis.gensim
    vis = pyLDAvis.gensim.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary_LDA)
    pyLDAvis.enable_notebook()
    pyLDAvis.display(vis)
