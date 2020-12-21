# Bayesian Reranking

Information Retrieval Project, 2020 @ Radboud University

The main file of this project is `src/rerank.py`.
It produces a baseline ranking using Anserini's BM25 implementation, and then re-ranks this initial ranking using topic modelling and a given re-ranking strategy.
All relative paths currently used in the scripts assume you are running from the `src` folder.

There are several other scripts for running analyses and plotting results.
There are also several scripts that demo the functionality of Anserini or LDA.

For our findings, see the [report](./report.pdf).

## Indexing

Our indexing command:

```
target/appassembler/bin/IndexCollection -collection WashingtonPostCollection -input ../WashingtonPost.v2/data -index indexes/lucene-wapost.v2.pos+docvectors+raw -generator WashingtonPostGenerator -threads 1 -storePositions -storeDocvectors -storeRaw
```

This produces a Lucene index via Anserini. 
Because you need permission to use the WashingtonPost, our index is not linked in this repository.



Topics and qrels for Common Core 2018:

- [CC2018 Topics](https://trec.nist.gov/data/core/topics2018.txt)
- [CC2018 Qrels]( https://trec.nist.gov/data/core/qrels2018.txt )
- [Anserini already has these built in]( https://github.com/castorini/anserini/tree/master/src/main/resources/topics-and-qrels )

## Handy Links

- [Anserini](https://github.com/castorini/anserini)
- [Pyserini](https://github.com/castorini/pyserini)
- [Anserini (eval) tools](https://github.com/castorini/anserini-tools)
- [ Anserini Common Indexing Options ](https://github.com/castorini/anserini/blob/master/docs/common-indexing-options.md)
- [ Regressions for Washington Post]( https://github.com/castorini/anserini/blob/master/docs/regressions-core18.md )
- [Trec Eval](https://github.com/usnistgov/trec_eval)
- [Qrels format](https://trec.nist.gov/data/qrels_eng/)

## Q&A

Error after importing SimpleSearcher from pyserini.search 

> ImportError: DLL load failed: Kan opgegeven module niet vinden.

[Solution]( https://stackoverflow.com/questions/20970732/jnius-1-1-import-error ): put `C:\Program Files (x86)\Java\jdk[YOUR JDK VERSION]\jre\bin\server` in your SYSTEM variables (not your user variables).
