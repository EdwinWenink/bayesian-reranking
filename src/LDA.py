'''
Reranking with Latent Dirichlet Analysis
----------------------------------------
This script does not contain the actual reranking 
but is a playground for the Bayesian procedure until convergence
''' 

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import make_multilabel_classification
from collections import defaultdict
import numpy as np

# This produces a feature matrix of token counts, similar to what
# CountVectorizer would produce on text.
X, _ = make_multilabel_classification(random_state=0)  # 100 samples, 20 features

def map_to_topic(X):
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
        lda = LatentDirichletAllocation(n_components=k, random_state=0)
        y_pred = lda.fit_transform(X)
        argmax = np.array( list(map( lambda x: np.argmax(x), y_pred)))
        topics, topic_counts = np.unique(argmax, return_counts=True)
        return topics, topic_counts, argmax

    k = len(X)  # init: k=N
    prev = np.zeros(k)
    i = 1

    # Find starting topics
    print(f"Iteration {i}: running with k={k}")
    lda = LatentDirichletAllocation(n_components=k, random_state=0)
    y_pred = lda.fit_transform(X)
    argmax = np.array( list(map( lambda x: np.argmax(x), y_pred)))
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

docs_per_topic = map_to_topic(X)
print(docs_per_topic)

# After this step, we need to order the topics on importance to determine picking order for reranking
