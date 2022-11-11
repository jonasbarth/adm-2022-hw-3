"""Module for the top k index"""
import math
from collections import Counter
from queue import PriorityQueue

from scipy import spatial

from index import Index, preprocess


class DocumentScore:
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

            new_value = []
            for doc_score in value:
                idf_score = math.log(self.n_total_documents / len(value))
                tf_idf = doc_score.score * idf_score

                doc_score.score = tf_idf

            self.index[key] = list(self.index[key])
            self.index[key].sort(key=lambda doc_score: doc_score.document_name)
            # new_value.sort(key=lambda doc_score: doc_score[0])
            # self.index[key] = new_value

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

        for word in query:
            tf = 1 / counter[word]
            idf = math.log(self.n_total_documents / len(self.index[word]))
            query_tf_idf.append(tf * idf)

        # 1 find all the word docs pairs in the index that match the query
        found = {word: self.get(word) for word in query}
        """
        all_words_in_docs = set.intersection(*map(set, found.values()))

        ranked = PriorityQueue(maxsize=k)
        for doc in all_words_in_docs:
            dist = spatial.distance.cosine(query_tf_idf, self.find_doc_vec(query, doc))
            ranked.put((dist, doc.document_name))

        return ranked"""
        # all_doc_scores =
        # 2 find all documents that have all words
        # collect ids
        """ids = []
        for document_scores in found.values():
            ids.append([document for document, _ in document_scores])

        # intersect on ids
        common_ids = set.intersection(*map(set, ids))

        # find tuples from ids
        # filter out tuples that don't have the common id
        found = {word: list(filter(lambda doc: doc[0] in common_ids, found[word])) for word in found}


        # 3 compute the cosine similarity for each document and add to a heap
        print(found)"""

        # for every

        # new approach
        # indeces to walk through the index

        indeces = [0] * len(query)

        # the lists we want to walk through
        found = {word: self.get(word) for word in query}
        all_doc_scores = list(found.values())
        index_end = False

        min_index = 0

        top_k = PriorityQueue(maxsize=k)

        while not index_end:

            indexed_docs = []
            for i, index_doc_scores in enumerate(zip(indeces, all_doc_scores)):
                index, doc_scores = index_doc_scores
                indexed_docs.append([i, index, doc_scores[index]])

            document_names = list(map(lambda t: t[-1].document_name, indexed_docs))
            if all(name == document_names[0] for name in document_names):
                # get vector
                tf_idf_vec = [row[-1].score for row in indexed_docs]
                # compute cosine
                # print("Putting an item")
                if top_k.full():
                    top_k.get()
                top_k.put((spatial.distance.cosine(query_tf_idf, tf_idf_vec), indexed_docs[0][-1].document_name))

            i, index, doc = min(indexed_docs, key=lambda doc: doc[-1].document_name)
            indeces[i] += 1

            index_end = indeces[i] == len(all_doc_scores[i])

        return [top_k.get() for _ in range(top_k.qsize())][::-1]

    def find_doc_vec(self, words, document):
        found = {word: self.get(word) for word in words}

        doc_vec = []
        for doc_scores in found.values():
            for doc_score in doc_scores:
                if doc_score.document_name == document.document_name:
                    doc_vec.append(doc_score.score)

        return doc_vec
