"""Module for a super class of a index used in a search engine."""

import json
import os
from abc import abstractmethod

from index import preprocess


class Index:
    """A basic inverted index."""

    def __init__(self):
        self.index = {}

    @staticmethod
    def create_from(documents, words):
        index = Index()
        for name, desc in zip(documents, words):

            desc = preprocess(desc)

            for token in desc:
                index.put(token, name)

        return index


    def put(self, word_id, document):
        """Puts a document into the inverted index at the word_id.

        :args
        word_id - the word for which the document will be added.
        document - the unique document name that will be added to the word in the index.
        """
        try:
            self.index[word_id].add(document)

        except KeyError:
            documents = set()
            documents.add(document)
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

    def load(self, path):
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        file_name = 'conjunctive_index.json'
        full_path = f'{path}/{file_name}'

        with open(full_path, 'r') as file:
            self.index = json.load(file)

    def save(self, path):
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        file_name = 'conjunctive_index.json'
        full_path = f'{path}/{file_name}'

        with open(full_path, 'w') as file:
            json.dump(self.index, file)

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
