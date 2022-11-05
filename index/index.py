"""Module for a super class of a index used in a search engine."""

from abc import ABC, abstractmethod
import json
import os


class Index(ABC):
    """Abstract Base Class for a search index."""

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

    @abstractmethod
    def put(self, word_id, document: str):
        """Puts a document into the inverted index at the word_id.

        :args
        word_id - the word for which the document will be added.
        document - the unique document name that will be added to the word in the index.
        """
        pass

    @abstractmethod
    def get(self, word_id: int):
        """Gets a list of documents that belong to the given word.

        :args
        word_id - the word for which the list of documents will be fetched.

        :raises
        a KeyError if the word does not exist in the index.
        """
        pass
