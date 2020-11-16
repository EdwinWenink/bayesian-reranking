# Bayesian Reranking

Information Retrieval Project, 2020 @ Radboud University

## Planning

Deadline: 21 December, 23:59pm

## Relevant papers

- *"Read Smart Stuff here"* by Smarty McSmartFace
- TODO

## Links

### Anserini/Pyserini

- [Anserini](https://github.com/castorini/anserini)
- [Pyserini](https://github.com/castorini/pyserini)
    * See README.md for an easy guide
- [Anserini Example Notebooks](https://github.com/castorini/anserini-notebooks)
- [Anserini (eval) tools](https://github.com/castorini/anserini-tools)
- [Anserini pre-built indexes](https://git.uwaterloo.ca/jimmylin/anserini-indexes)
    * N.B. also contains a readme.txt for the command to build the index with Anserini!
- [Anserini at TREC 2018: CENTRE, Common Core, and News Tracks]( https://cs.uwaterloo.ca/~jimmylin/publications/Yang_Lin_TREC2018.pdf )

### Indexing

Indexing on Washington Post:

- [ Anserini Common Indexing Options ](https://github.com/castorini/anserini/blob/master/docs/common-indexing-options.md)
- [ Regressions for Washington Post]( https://github.com/castorini/anserini/blob/master/docs/regressions-core18.md )
    * Also shows how to use `trec_eval` using the topics and qrels!
- [Example project indexing WaPost](https://github.com/PepijnBoers/background-linking)

Example indexing command from WaPost regression page:

```
nohup sh target/appassembler/bin/IndexCollection -collection WashingtonPostCollection \
 -input /path/to/core18 \
 -index indexes/lucene-index.core18.pos+docvectors+raw \
 -generator WashingtonPostGenerator \
 -threads 1 -storePositions -storeDocvectors -storeRaw \
  >& logs/log.core18 &
```

Our indexing command:

```
target/appassembler/bin/IndexCollection -collection WashingtonPostCollection -input ../WashingtonPost.v2/data -index indexes/lucene-wapost.v2.pos+docvectors+raw -generator WashingtonPostGenerator -threads 1 -storePositions -storeDocvectors -storeRaw
```

### Evaluation

- [Blog post on how to use TREC eval](http://www.rafaelglater.com/en/post/learn-how-to-use-trec_eval-to-evaluate-your-information-retrieval-system)
- [Qrels format](https://trec.nist.gov/data/qrels_eng/)

Topics and qrels for Common Core 2018:

- [CC2018 Topics](https://trec.nist.gov/data/core/topics2018.txt)
- [CC2018 Qrels]( https://trec.nist.gov/data/core/qrels2018.txt )
- [Anserini already has these built in]( https://github.com/castorini/anserini/tree/master/src/main/resources/topics-and-qrels )


## Fixes

Error after importing SimpleSearcher from pyserini.search 

> ImportError: DLL load failed: Kan opgegeven module niet vinden.

[Solution]( https://stackoverflow.com/questions/20970732/jnius-1-1-import-error ): put `C:\Program Files (x86)\Java\jdk[YOUR JDK VERSION]\jre\bin\server` in your SYSTEM variables (not your user variables).
