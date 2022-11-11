"""Module for the top k index"""
import math
from collections import Counter
from queue import PriorityQueue

import numpy as np
from numpy.linalg import norm

from index import Index, preprocess


class DocumentScore:
    """A class for storing a document and a document score."""

    id: str
    score: float

    def __init__(self, id, score):
        self.id = id
        self.score = score

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return other.id == self.id

    def __repr__(self):
        return f'{self.id}, {self.score}'

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __le__(self, other):
        return self.id <= other.id


class TfIdfIndex(Index):
    """An index that uses TF-IDF scores."""

    def __init__(self, n_total_documents: int):
        super().__init__()
        self.n_total_documents = n_total_documents

    @staticmethod
    def create_from(document_ids, words):
        index = TfIdfIndex(len(document_ids))
        for name, desc in zip(document_ids, words):

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

        top_k = PriorityQueue(maxsize=k+1)

        while not index_end:

            # 1 find the elements the current indeces are pointing
            indexed_docs = []
            for i, index_doc_scores in enumerate(zip(indeces, all_doc_scores)):
                index, doc_scores = index_doc_scores
                indexed_docs.append([i, index, doc_scores[index]])

            document_ids = list(map(lambda t: t[-1].id, indexed_docs))

            # 2 if all the items the current indeces point to, are the same, we save the distance to the query in the heap
            if all(id == document_ids[0] for id in document_ids):
                tf_idf_vec = [row[-1].score for row in indexed_docs]

                if top_k.full():
                    top_k.get()

                cosine = np.dot(query_tf_idf, tf_idf_vec) / (norm(query_tf_idf) * norm(tf_idf_vec))
                top_k.put((cosine, indexed_docs[0][-1].id))

            # 3 increase the minimum index
            i, index, doc = min(indexed_docs, key=lambda doc: doc[-1].id)
            indeces[i] += 1

            # 4 we want to stop when either index has reached the end
            index_end = indeces[i] == len(all_doc_scores[i])

        top_k.get()
        # higher similarities should come first
        return [top_k.get() for _ in range(top_k.qsize())][::-1]
