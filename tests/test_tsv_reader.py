"""Unit tests for reading tsv files"""
import codecs
import os

import pytest

from parse import PlaceParser
from reader import read_place_desc
from writer import write_place_to_tsv


@pytest.fixture
def path():
    return './places.tsv'


@pytest.fixture
def place():
    with codecs.open("./resources/City Hall Station – New York, New York - Atlas Obscura.html", "r", "utf-8") as file:
        html = file.read()
        parser = PlaceParser(html)
        return parser.parse()


@pytest.fixture(autouse=True)
def assert_no_file():
    path = './places.tsv'
    assert not os.path.exists(path)
    yield
    os.remove(path)
    assert not os.path.exists(path)


def test_that_description_is_read(place):
    path = write_place_to_tsv('./', [place])

    descriptions = read_place_desc(path)

    assert len(descriptions) == 1