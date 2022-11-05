"""Module for a conjunctive index"""
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

    def query(self, query):
        # Put the query code here
        pass
