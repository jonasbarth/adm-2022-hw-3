"""Module for a conjunctive index"""
import os
import json

#TODO create Index super class
class ConjunctiveIndex:
    """Class for building a conjunctive index."""
    def __init__(self):
        self.index = {}

    #TODO make the path check into a decorator
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

    def query(self, query_words):
        pass
