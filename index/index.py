"""Module for a super class of a index used in a search engine."""

from abc import ABC, abstractmethod
import json
import os


class Index(ABC):
    """Abstract Base Class for a search index."""

    # TODO make the path check into a decorator
    @abstractmethod
    def load(self, path):
        """Loads a stored conjunctive index."""
        pass

    @abstractmethod
    def save(self, path):
        """Saves the conjunctive index into a file."""
        pass

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

    @abstractmethod
    def query(self, query):
        """Runs a query against the index.

        :args
        query - a query string.

        :returns
        a list of document ids that match the query.
        """
