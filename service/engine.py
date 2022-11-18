"""Python module containing logic for the Atlas Obscura search engine."""
from queue import PriorityQueue

import pandas as pd

from index import Index
from service import PlaceService
from util import get_location, calculate_distance_score, calculate_popularity_score


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

        return all_places[['name', 'desc', 'url', 'address', 'similarity', 'lat', 'lon', 'num_people_visited', 'num_people_want']]

    def query_custom(self, query, top_k, proximity=False, popularity=False):

        if not (proximity or popularity):
            raise ValueError("Must specify either close_to_me or popularity.")

        place_names = self.index.query(query)
        places = [self.place_service.get(place_name) for place_name in place_names]

        all_places = pd.concat(places)

        queue = PriorityQueue(maxsize=top_k)

        if proximity and popularity:
            all_places = all_places[['id', 'num_people_visited', 'num_people_want', 'lat', 'lon']]
            queue = _get_proximity_and_popularity_queue(all_places, top_k)

        elif proximity:
            all_places = all_places[['id', 'lat', 'lon']]
            queue = _get_proximity_queue(all_places, top_k)

        elif popularity:
            all_places = all_places[['id', 'num_people_visited', 'num_people_want']]
            queue = _get_popularity_queue(all_places, top_k)

        scores_ids = [queue.get() for _ in range(queue.qsize())][::-1]
        places = [self.place_service.get(place_id) for _, place_id in scores_ids]
        similarity_scores = [similarity for similarity, _ in scores_ids]

        ranked_places = pd.concat(places)
        ranked_places['similarity'] = similarity_scores

        return ranked_places[['name', 'desc', 'address', 'similarity', 'lat', 'lon', 'num_people_visited', 'num_people_want']]


def _get_popularity_queue(matched_places, top_k):
    queue = PriorityQueue(maxsize=top_k)

    total_people_visited = matched_places.num_people_visited.sum()
    total_people_want = matched_places.num_people_want.sum()

    for row in matched_places.values:
        id, num_people_visited, num_people_want = row

        num_people_visited = 1 if num_people_visited == 0 else num_people_visited
        num_people_want = 1 if num_people_want == 0 else num_people_want
        # more people visit, the better

        # means that if either visited or want is 0, we will have a score of 0
        popularity_score = calculate_popularity_score(num_people_visited, total_people_visited, num_people_want,
                                                      total_people_want)

        _add_to_queue(queue, popularity_score, id)

    return queue


def _get_proximity_queue(matched_places, top_k):
    queue = PriorityQueue(maxsize=top_k)

    current_loc = get_location()
    current_coords = (current_loc['latitude'], current_loc['longitude'])

    for id_coords in matched_places.values:
        id, lat, lon = id_coords

        distance_score = calculate_distance_score(current_coords, (lat, lon))

        _add_to_queue(queue, distance_score, id)

    return queue


def _get_proximity_and_popularity_queue(matched_places, top_k):
    queue = PriorityQueue(maxsize=top_k)

    current_loc = get_location()
    current_coords = (current_loc['latitude'], current_loc['longitude'])

    total_people_visited = matched_places.num_people_visited.sum()
    total_people_want = matched_places.num_people_want.sum()

    for row in matched_places.values:
        id, num_people_visited, num_people_want, lat, lon = row

        distance_score = calculate_distance_score(current_coords, (lat, lon))

        num_people_visited = 1 if num_people_visited == 0 else num_people_visited
        num_people_want = 1 if num_people_want == 0 else num_people_want
        popularity_score = calculate_popularity_score(num_people_visited, total_people_visited, num_people_want,
                                                      total_people_want)

        score = distance_score * popularity_score

        _add_to_queue(queue, score, id)

    return queue


def _add_to_queue(queue, score, id):
    if queue.full():
        lowest_score, lowest_id = queue.get()

        if lowest_score > score:
            score = lowest_score
            id = lowest_id

    queue.put((score, id))
