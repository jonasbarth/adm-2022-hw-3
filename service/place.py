"""A module for reading places."""
from util import read_places


class PlaceService:
    """A class that exposes places from atlas obscura."""

    def __init__(self):
        self.places = None

    def get(self, id):
        """Returns the places that match the name."""
        return self.places[self.places.id == id]

    def load(self, path):
        """Loads the place service from a specified path."""
        self.places = read_places(path)
