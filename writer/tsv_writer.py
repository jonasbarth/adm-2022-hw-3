"""Module for writing Atlas Obscura places to tsv files"""
from domain import Place
import os


def write_place_to_tsv(path: str, places):
    """Writes a Place object into a tsv file at the specified path.

    :args
    path - the directory path where the file should be written.
    places - a list of Place objects that will be written to the file.

    :returns
    the path of the saved tsv file
    """

    file_name = 'places.tsv'
    full_path = f'{path}{file_name}'
    if not os.path.isdir(path):
        raise OSError('The path: {path} does not exist.')

    headers = '\t'.join(vars(places[0]).keys())
    headers = f'{headers}\n'

    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(headers)

        for place in places:
            line = []
            for value in vars(place).values():
                if isinstance(value, list):
                    value = ','.join(value)

                line.append(value)

            line = '\t'.join(map(str, line))
            file.write(f'{line}\n')

    return full_path
