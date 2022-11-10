"""Module for writing Atlas Obscura places to tsv files"""

import pandas as pd


def write_places_to_tsv(path: str, places):
    """Writes a Place object into a tsv file at the specified path.

    :args
    path - the directory path where the file should be written.
    places - a list of Place objects that will be written to the file.

    :returns
    the path of the saved tsv file
    """
    columns = [*vars(places[0]).keys()]
    places = list(map(lambda p: p.__dict__, places))
    full_path = f'{path}/places.tsv'

    for place in places:
        for key, value in place.items():
            if isinstance(value, list):
                new_value = ','.join(value)
                place[key] = new_value

    places_df = pd.DataFrame.from_records(places, columns=columns)

    places_df.to_csv(full_path, sep='\t')

    return full_path
