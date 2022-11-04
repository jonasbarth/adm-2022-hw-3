"""Module for writing Atlas Obscura places to tsv files"""
from domain import Place
import os


def write_place_to_tsv(path: str, place: Place):
    """Writes a Place object into a tsv file at the specified path.

    :args
    path - the directory path where the file should be written, without the name of the file.
    place - a Place object that will be written.

    :returns
    the path of the saved tsv file
    """

    formatted_place_name = place.name.lower().replace(' ', '_')
    file_name = f'{formatted_place_name}.tsv'

    if not os.path.isdir(path):
        raise OSError('The path: {path} does not exist.')

    full_path = f'{path}{file_name}'
    with open(full_path, 'w') as file:
        line = []

        for value in vars(place).values():
            if isinstance(value, list):
                value = ','.join(value)

            line.append(value)

        line = '\t'.join(map(str, line))
        file.write(line)

    return full_path
