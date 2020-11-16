
def print_top_n_results(hits, n):
    for i in range(0, n):
        print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')


def top_n_words(doc_vector, n=10):
    # Values of doc vector can include None, which blocks comparison
    # Make this sortable by including this as a Boolean
    for i, (k, v) in enumerate(sorted(doc_vector.items(), key=lambda x: (x[1] is not None, x[1]), reverse=True)):
        print(f"{i+1}. {k}:{v}")
        if i==n: break


def print_topic(topics, id=None):
    """
    By default prints information on all topics
    If valid id is provided, prints full info on a single topic
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

