"""Module for a conjunctive index"""
import os
import json
from queue import PriorityQueue


# TODO create Index super class
class ConjunctiveIndex:
    """Class for building a conjunctive index."""

    def __init__(self):
        self.index = {}

    # TODO make the path check into a decorator
    def load(self, path):
        """Loads a stored conjunctive index."""
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        file_name = 'conjunctive_index.json'
        full_path = f'{path}/{file_name}'

        with open(full_path, 'r') as file:
            self.index = json.load(file)

    def save(self, path):
        """Saves the conjunctive index into a file."""
        if not os.path.isdir(path):
            raise OSError(f'The path: {path} does not exist.')

        file_name = 'conjunctive_index.json'
        full_path = f'{path}/{file_name}'
        with open(full_path, 'w') as file:
            json.dump(self.index, file)

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

    def query(self, query_words):
        pass
