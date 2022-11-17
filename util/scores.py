"""A module for calculating similarity and ranking scores."""
from util import get_distance
from util.location import max_distance_on_earth


def calculate_distance_score(coords1, coords2):
    """Calculates the distance score for two pairs of lat,lon coordinates."""

    distance = get_distance(coords1, coords2)

    distance_score = (max_distance_on_earth - distance) / max_distance_on_earth

    return distance_score


def calculate_popularity_score(num_people_visited, total_people_visited, num_people_want, total_people_want):
    """Calculates the popularity score for an Atlas Obscura place."""

    popularity_score = (1/2) * (num_people_visited / total_people_visited + num_people_want / total_people_want)
    return popularity_score
