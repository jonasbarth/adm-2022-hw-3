"""Python module containing logic for the Atlas Obscura search engine."""
import math
from queue import PriorityQueue

import pandas as pd

from index import Index
from service import PlaceService
from util import get_location, get_distance, calculate_distance_score, calculate_popularity_score
from util.location import max_distance_on_earth


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

    def query_custom(self, query, top_k, close_to_me=False, popularity=False):

        if not (close_to_me or popularity):
            raise ValueError("Must specify either close_to_me or popularity.")

        place_names = self.index.query(query)
        places = [self.place_service.get(place_name) for place_name in place_names]

        all_places = pd.concat(places)

        queue = PriorityQueue(maxsize=top_k)

        if close_to_me and popularity:
            current_loc = get_location()
            current_coords = (current_loc['latitude'], current_loc['longitude'])

            all_places = all_places[['id', 'num_people_visited', 'num_people_want', 'lat', 'lon']]

            total_people_visited = all_places.num_people_visited.sum()
            total_people_want = all_places.num_people_want.sum()

            for row in all_places.values:
                id, num_people_visited, num_people_want, lat, lon = row

                distance_score = calculate_distance_score(current_coords, (lat, lon))

                num_people_visited = 1 if num_people_visited == 0 else num_people_visited
                num_people_want = 1 if num_people_want == 0 else num_people_want
                popularity_score = calculate_popularity_score(num_people_visited, total_people_visited, num_people_want, total_people_want)

                score = distance_score * popularity_score

                if queue.full():
                    lowest_score, lowest_id = queue.get()

                    if lowest_score > score:
                        score = lowest_score
                        id = lowest_id

                queue.put((score, id))

        elif close_to_me:
            current_loc = get_location()
            current_coords = (current_loc['latitude'], current_loc['longitude'])

            all_places = all_places[['id', 'lat', 'lon']]
            for id_coords in all_places.values:
                id, lat, lon = id_coords

                distance_score = calculate_distance_score(current_coords, (lat, lon))

                if queue.full():
                    lowest_score, lowest_id = queue.get()

                    if lowest_score > distance_score:
                        distance_score = lowest_score
                        id = lowest_id


                queue.put((distance_score, id))

        elif popularity:
            all_places = all_places[['id', 'num_people_visited', 'num_people_want']]
            total_people_visited = all_places.num_people_visited.sum()
            total_people_want = all_places.num_people_want.sum()
            for row in all_places.values:
                id, num_people_visited, num_people_want = row

                num_people_visited = 1 if num_people_visited == 0 else num_people_visited
                num_people_want = 1 if num_people_want == 0 else num_people_want
                # more people visit, the better

                # means that if either visited or want is 0, we will have a score of 0
                popularity_score = calculate_popularity_score(num_people_visited, total_people_visited, num_people_want, total_people_want)

                if queue.full():
                    lowest_score, lowest_id = queue.get()

                    if lowest_score > popularity_score:
                        popularity_score = lowest_score
                        id = lowest_id

                queue.put((popularity_score, id))

        scores_ids = [queue.get() for _ in range(queue.qsize())][::-1]
        places = [self.place_service.get(place_id) for _, place_id in scores_ids]
        similarity_scores = [similarity for similarity, _ in scores_ids]

        ranked_places = pd.concat(places)
        ranked_places['similarity'] = similarity_scores

        return ranked_places[['name', 'desc', 'address', 'similarity']]
