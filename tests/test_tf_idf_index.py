"""Tests for the TF IDF Index"""
import math

from index import TfIdfIndex

from index import preprocess

def test_that_tf_idf_score_correct():
    documents = ["doc1", "doc2", "doc3"]
    words = ["doc doc", "doc man", "man doc"]

    doc1_tf = 2 / len(preprocess(words[0], unique=False))
    doc1_idf = math.log(3 / 2)

    doc_tf_idf = doc1_tf * doc1_idf

    index = TfIdfIndex.create_from(documents, words)

    index.query_top_k("doc man", 2)
    index.get("doc man")

