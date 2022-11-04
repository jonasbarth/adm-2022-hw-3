"""A module for reading tsv files about places."""

import pandas as pd


def read_place_desc(path: str):
    """Reads all the place description stored in a tsv file from the given path and returns them."""

    place = pd.read_csv(path, sep='\t', usecols=['name', 'desc'], encoding='utf-8')
    return place.name, place.desc
