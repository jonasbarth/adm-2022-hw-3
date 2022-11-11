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

        all_places = pd.concat(places)
        return all_places[['name', 'desc', 'url']]


    def query_top_k(self, query, top_k):
        result = self.index.query_top_k(query, top_k)
        places = [self.place_service.get(place_name) for _, place_name in result]
        similarity_scores = [similarity for similarity, _ in result]

        all_places = pd.concat(places)
        all_places['similarity'] = similarity_scores

        return all_places[['name', 'desc', 'url', 'similarity']]



