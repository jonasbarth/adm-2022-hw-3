"""Unit tests for tsv writer"""
import codecs
import os

import pytest

from parse import PlaceParser
from util import write_places_to_tsv


@pytest.fixture
def place():
    with codecs.open("./resources/City Hall Station – New York, New York - Atlas Obscura.html", "r", "utf-8") as file:
        html = file.read()
        parser = PlaceParser(html)
        return parser.parse()


@pytest.fixture(autouse=True)
def assert_no_file():
    path = './city_hall_station.tsv'
    assert not os.path.exists(path)
    yield
    assert not os.path.exists(path)


def test_that_file_is_created(place):
    tsv_path = write_places_to_tsv('./', [place, place])
    os.remove(tsv_path)
