"""Python module containing logic for the Atlas Obscura search engine."""
import pandas as pd

from index import Index
from service import PlaceService


class SearchEngine:
    """A search engine that can be configured to use different indeces."""

    def __init__(self, index: Index, place_service: PlaceService):
        self.index = index
        self.place_service = place_service

    def query(self, query):
        """Runs a query against the search engine."""
        place_names = self.index.query(query)
        places = [self.place_service.get(place_name) for place_name in place_names]

        return pd.concat(places)




