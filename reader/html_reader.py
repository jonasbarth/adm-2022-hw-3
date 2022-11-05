"""Module for reading html files."""
import codecs


def read_html_from(path: str):
    """Reads the html file at the specified path and returns a string of the html."""

    with codecs.open(path, "r", "utf-8") as file:
        return file.read()