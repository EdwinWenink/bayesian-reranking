"""
Utility functions
"""

class Utils():
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


    def write_ranking(self, query_id, doc_ids, scores, run_name):
        """
        Writes ranking for results of a *single* query
        
        Assumes inputs are already ordered on rank
        Length of doc_ids and scores should match

        Format: query-id Q0 document-id rank score RUN-NAME
        -----
        Returns None
        """
        with open(f"../results/results-{run_name}.txt", encoding="utf-8", mode="w") as f:
            for i in range(len(doc_ids)):
                f.write(f"{query_id} Q0 {doc_ids[i]} {i+1} {scores[i]} {run_name}\n")
        print(f"Wrote results to /results/results-{run_name}.txt")


    def write_rankings(self, query_ids, doc_ids, scores, run_name):
        """
        Writes ranking for results of *multiple* queries

        doc_ids and scores should be lists with len(query_ids) sublists
        These sublists are are assumed to be sorted on rank
        and should have the same length

        Format: query-id Q0 document-id rank score RUN-NAME
        -----
        Returns None
        """
        with open(f"../results/results-{run_name}.txt", encoding="utf-8", mode="w") as f:
            for i, query_id in enumerate(query_ids):
                for j in range(len(doc_ids[i])):
                    f.write(f"{query_id} Q0 {doc_ids[i][j]} {j+1} {scores[i][j]} {run_name}\n")
        print(f"Wrote results to /results/results-{run_name}.txt")

