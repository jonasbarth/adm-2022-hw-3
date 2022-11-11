"""A module for reading tsv files about places."""

import pandas as pd


def read_place_desc(path: str):
    """Reads all the place description stored in a tsv file from the given path and returns them."""

    place = pd.read_csv(path, sep='\t', usecols=['name', 'desc'], encoding='utf-8')
    return place.name, place.desc


def read_places(path: str):
    """Reads places from the given path."""
    return pd.read_csv(path, sep='\t', encoding='utf-8', index_col=0)
