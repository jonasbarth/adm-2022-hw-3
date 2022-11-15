"""Module for a super class of a index used in a search engine."""

import json
import pickle
import os
from abc import abstractmethod

from index import preprocess


class Index:
    """A basic inverted index."""

    def __init__(self):
        self.index = {}

    @staticmethod
    def create_from(document_ids, words):
        index = Index()
        for id, desc in zip(document_ids, words):

            desc = preprocess(desc)

            for token in desc:
                index.put(token, id)

        return index

    @staticmethod
    def load_from(path):
        if not os.path.isfile(path):
            raise OSError(f'The file: {path} does not exist.')

        with open(path, 'rb') as file:
            index = pickle.load(file)

        return index

    def put(self, word_id, document_id):
        """Puts a document into the inverted index at the word_id.

        :args
        word_id - the word for which the document will be added.
        document - the unique document name that will be added to the word in the index.
        """
        try:
            self.index[word_id].add(document_id)

        except KeyError:
            documents = set()
            documents.add(document_id)
            self.index[word_id] = documents

    def get(self, word_id: int):
        """Gets a list of documents that belong to the given word.

        :args
        word_id - the word for which the list of documents will be fetched.

        :raises
        a KeyError if the word does not exist in the index.
        """
        try:
            return self.index[word_id]

        except KeyError:
            raise KeyError(f'The word: {word_id}, does not exist in the index.')

    def save(self, path, name):
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        full_path = f'{path}/{name}.pickle'

        with open(full_path, 'wb') as file:
            pickle.dump(self, file)

    def query(self, query):
        """Runs a query against the index.

        :args
        query - a query string.

        :returns
        a list of document ids that match the query.
        """
        query = preprocess(query)
        found = []
        for word in query:
            try:
                found.append(self.index[word])
            except KeyError:
                return []

        return set.intersection(*map(set, found))

    @abstractmethod
    def query_top_k(self, query, k):
        """Runs a query against the index and returns the top k documents.

        :args
        query - a query string.
        k - an integer specifying the number of top ranked documents to return.

        :returns
        a list of length k of document ids that match the query."""
