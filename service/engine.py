"""Python module containing logic for the Atlas Obscura search engine."""
import math
from queue import PriorityQueue

import pandas as pd

from index import Index
from service import PlaceService
from util import get_location, get_distance


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

    def query_custom(self, query, top_k, close_to_me=False):
        place_names = self.index.query(query)
        places = [self.place_service.get(place_name) for place_name in place_names]

        all_places = pd.concat(places)

        queue = PriorityQueue(maxsize=top_k)
        if close_to_me:
            current_loc = get_location()
            current_coords = (current_loc['latitude'], current_loc['longitude'])

            for id_coords in all_places[['id', 'lat', 'lon']].values:
                id = id_coords[0]
                coords = id_coords[1:]

                distance = get_distance(current_coords, coords)

                score = -distance

                if queue.full():
                    furthest_away_score, furthest_away_id = queue.get()

                    if furthest_away_score > score:
                        score = furthest_away_score
                        id = furthest_away_id

                queue.put((score, id))

        scores_ids = [queue.get() for _ in range(queue.qsize())][::-1]
        places = [self.place_service.get(place_id) for _, place_id in scores_ids]
        similarity_scores = [similarity for similarity, _ in scores_ids]

        ranked_places = pd.concat(places)
        ranked_places['similarity'] = similarity_scores

        return ranked_places[['name', 'desc', 'address', 'similarity']]






