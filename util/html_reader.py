"""Module for reading html files."""
import codecs
from os import listdir

from joblib import Parallel, delayed


def read_htmls_in(directory: str, n_jobs=7):
    """Reads all the html files in the subdirectories of the provided directory, in parallel."""
    folders = listdir(directory)
    html_paths = [f'{directory}/{file}/{html}' for file in folders for html in listdir(f'{directory}/{file}')]

    def parallel(html_path):
        return read_html_from(html_path)

    all_htmls = Parallel(n_jobs=n_jobs)(delayed(parallel)(html_path) for html_path in html_paths)
    return all_htmls

def read_html_from(path: str):
    """Reads the html file at the specified path and returns a string of the html."""

    with codecs.open(path, "r", "utf-8") as file:
        return file.read()