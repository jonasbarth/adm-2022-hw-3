"""Module for a conjunctive index"""
import json
import os
from queue import PriorityQueue

from .index import Index


class ConjunctiveIndex(Index):
    """Class for building a conjunctive index."""

    def __init__(self):
        self.index = {}

    def put(self, word_id, document: str):
        """Puts a document into the inverted index at the word_id.

        :args
        word_id - the word for which the document will be added.
        document - the unique document name that will be added to the word in the index.
        """
        try:
            self.index[word_id].put(document)

        except KeyError:
            documents = PriorityQueue()
            documents.put(document)
            self.index[word_id] = documents

    def get(self, word_id: int):
        """Gets a list of documents that belong to the given word.

        :args
        word_id - the word for which the list of documents will be fetched.

        :raises
        a KeyError if the word does not exist in the index.
        """
        try:
            return self.index[word_id].queue

        except KeyError:
            raise KeyError(f'The word: {word_id}, does not exist in the index.')

    def load(self, path):
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        file_name = 'conjunctive_index.json'
        full_path = f'{path}/{file_name}'

        with open(full_path, 'r') as file:
            index = json.load(file)
            self.index = {k: PriorityQueue(v) for k, v in index.items()}

    def save(self, path):
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        file_name = 'conjunctive_index.json'
        full_path = f'{path}/{file_name}'

        index_with_list = {k: v.queue for k, v in self.index.items()}

        with open(full_path, 'w') as file:
            json.dump(index_with_list, file)

    def query(self, query):
        # Put the query code here
        pass
