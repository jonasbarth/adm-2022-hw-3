"""Module for the top k index"""
import math
from collections import Counter
from queue import PriorityQueue

import numpy as np
from numpy.linalg import norm
from scipy import spatial

from index import Index, preprocess


class DocumentScore:
    """A class for storing a document and a document score."""

    document_name: str
    score: float

    def __init__(self, document_name, score):
        self.document_name = document_name
        self.score = score

    def __hash__(self):
        return hash(self.document_name)

    def __eq__(self, other):
        return other.document_name == self.document_name

    def __repr__(self):
        return f'{self.document_name}, {self.score}'

    def __lt__(self, other):
        return self.document_name < other.document_name

    def __gt__(self, other):
        return self.document_name > other.document_name

    def __ge__(self, other):
        return self.document_name >= other.document_name

    def __le__(self, other):
        return self.document_name <= other.document_name


class TfIdfIndex(Index):
    """An index that uses TF-IDF scores."""

    def __init__(self, n_total_documents: int):
        super().__init__()
        self.n_total_documents = n_total_documents

    @staticmethod
    def create_from(documents, words):
        index = TfIdfIndex(len(documents))
        for name, desc in zip(documents, words):

            desc = preprocess(desc, unique=False)

            counter = Counter(desc)

            for token in desc:
                tf = counter[token] / len(desc)
                doc_score = DocumentScore(name, tf)
                index.put(token, doc_score)

        index.postprocess()

        return index

    def postprocess(self):
        for key, value in self.index.items():

            for doc_score in value:
                idf_score = math.log(self.n_total_documents / len(value))
                tf_idf = doc_score.score * idf_score

                doc_score.score = tf_idf

            self.index[key] = list(self.index[key])
            self.index[key].sort()

    def query(self, query):
        query = preprocess(query)
        found = []
        for word in query:
            try:
                found.append(self.index[word])
            except KeyError:
                return []

        return set.intersection(*map(set, found))

    def query_top_k(self, query, k):

        query = preprocess(query)
        counter = Counter(query)

        query_tf_idf = []
        # compute the tf idf for the query
        for word in query:
            tf = counter[word] / len(query)
            idf = math.log(self.n_total_documents / len(self.index[word]))
            query_tf_idf.append(tf * idf)

        indeces = [0] * len(query)
        all_doc_scores = [self.get(word) for word in query]
        index_end = False

        top_k = PriorityQueue(maxsize=k)

        while not index_end:

            # 1 find the elements the current indeces are pointing
            indexed_docs = []
            for i, index_doc_scores in enumerate(zip(indeces, all_doc_scores)):
                index, doc_scores = index_doc_scores
                indexed_docs.append([i, index, doc_scores[index]])

            document_names = list(map(lambda t: t[-1].document_name, indexed_docs))

            # 2 if all the items the current indeces point to, are the same, we save the distance to the query in the heap
            if all(name == document_names[0] for name in document_names):
                tf_idf_vec = [row[-1].score for row in indexed_docs]

                if top_k.full():
                    top_k.get()

                cosine = np.dot(query_tf_idf, tf_idf_vec) / (norm(query_tf_idf) * norm(tf_idf_vec))
                top_k.put((cosine, indexed_docs[0][-1].document_name))

            # 3 increase the minimum index
            i, index, doc = min(indexed_docs, key=lambda doc: doc[-1].document_name)
            indeces[i] += 1

            # 4 we want to stop when either index has reached the end
            index_end = indeces[i] == len(all_doc_scores[i])

        # higher similarities should come first
        return [top_k.get() for _ in range(top_k.qsize())][::-1]
