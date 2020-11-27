"""
Utility functions
"""

from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Utils():
    def analyze(self, hits, query, n):
        index_reader = index.IndexReader('../../anserini/indexes/lucene-wapost.v2.pos+docvectors+raw')
        for i in range (0, n):
            doc = hits[i].raw
            analyzed_doc = index_reader.analyze(doc)
            print(analyzed_doc)

    def extract_keywords_of_doc(self, doc):
        # Like https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea
        # Extract candidate keywords/keyphrases
        # moet dezelfde analyze als anserini gebruiken
        n_gram_range = (3, 3)
        stop_words = "english" 
        count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
        candidates = count.get_feature_names()

        # Extract doc embedding & candidate keywords/keyphrases embeddings
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        doc_embedding = model.encode([doc])
        candidate_embeddings = model.encode(candidates)

        # Pick the top 5 keywords/keyphrases based on cosine similarity
        top_n = 5
        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
        print(keywords)

    def print_top_n_results(self, hits, n):
        """
        Works for results on a *single* query
        """
        for i in range(0, n):
            print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')


    def top_n_words(self, doc_vector, n=10):
        """
        Works for results on a *single* query
        """
        # Values of doc vector can include None, which blocks comparison
        # Make this sortable by including this as a Boolean
        for i, (k, v) in enumerate(sorted(doc_vector.items(), key=lambda x: (x[1] is not None, x[1]), reverse=True)):
            print(f"{i+1}. {k}:{v}")
            if i==n: break


    def print_topic(self, topics, id=None):
        """
        By default prints information on all topics
        If valid id is provided, prints full info on a single topic

        -------
        Returns None
        """
        print(f'{len(topics)} queries total\n')
        ids = topics.keys()
        if id:
            try:
                topic = topics[id]
                sep = '-'*(len(topic['title'])+10)
                print(f"TOPIC {id}: {topic['title']}\n{sep}")
                print(f"Description: {topic['description']}\n")
                print(f"Narrative: {topic['narrative']}\n")
            except:
                print("Provide valid id")
        else:
            for id in ids:
                topic = topics[id]
                sep = '-'*(len(topic['title'])+10)
                print(f"TOPIC {id}: {topic['title']}\n{sep}")
                print(f"Description: {topic['description']}\n")


    def write_rankings(self, query_ids, doc_ids, scores, run_name):
        """
        Writes ranking and scores for *multiple* queries

        query_ids: List[int]
        doc_ids: Dict[str, List[str]]
        scores: Dict[str, List[str]]

        Format: query-id Q0 document-id rank score run_name
        -----
        Returns None
        """
        with open(f"../results/results-{run_name}.txt", encoding="utf-8", mode="w") as f:
            for query_id in sorted(query_ids):
                for i in range(len(doc_ids[query_id])):
                    f.write(f"{query_id} Q0 {doc_ids[query_id][i]} {i+1} {scores[query_id][i]} {run_name}\n")
        print(f"Wrote results to /results/results-{run_name}.txt")

        analyze()

