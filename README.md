# Bayesian Reranking

Information Retrieval Project, 2020 @ Radboud University

## Planning

Deadline: 21 December, 23:59pm

## Relevant papers

## Links

- [Anserini](https://github.com/castorini/anserini)
- [Pyserini](https://github.com/castorini/pyserini)
    * See README.md for an easy guide
- [Anserini Example Notebooks](https://github.com/castorini/anserini-notebooks)
- [Anserini (eval) tools](https://github.com/castorini/anserini-tools)
- [Anserini pre-built indexes](https://git.uwaterloo.ca/jimmylin/anserini-indexes)
    * N.B. also contains a readme.txt for the command to build the index with Anserini!
- [Blog post on how to use TREC eval](http://www.rafaelglater.com/en/post/learn-how-to-use-trec_eval-to-evaluate-your-information-retrieval-system)

## Fixes

Error after importing SimpleSearcher from pyserini.search 

> ImportError: DLL load failed: Kan opgegeven module niet vinden.

[Solution]( https://stackoverflow.com/questions/20970732/jnius-1-1-i mport-error ): put `C:\Program Files (x86)\Java\jdk[YOUR JDK VERSION]\jre\bin\server` in your SYSTEM variables (not your user variables).
