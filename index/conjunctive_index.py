"""Module for a conjunctive index"""


class ConjunctiveIndex:

    # how to build?
    # add word, document
    def __init__(self):
        self.index = {}

    def load(self, path):
        """Loads a stored conjunctive index."""
        pass

    def save(self, path):
        """Saves the conjunctive index into a file."""

    def put(self, word_id: int, document: str):
        try:
            self.index[word_id].append(document)

        except KeyError:
            self.index[word_id] = [document]

    def get(self, word_id: int):
        try:
            return self.index[word_id]

        except KeyError:
            return []
