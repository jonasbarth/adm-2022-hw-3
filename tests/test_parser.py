"""Tests for the parser module"""
import codecs

import pytest

from parse import PlaceParser


@pytest.fixture
def parser():
    with codecs.open("./resources/City Hall Station – New York, New York - Atlas Obscura.html", "r", "utf-8") as file:
        html = file.read()
        parser = PlaceParser(html)

        parser.parse()
        return parser


def test_name_is_parsed(parser):
    assert parser.name == "City Hall Station"


def test_num_people_visited_is_parsed(parser):
    assert parser.num_people_visited == 1826


def test_num_people_want_is_parsed(parser):
    assert parser.num_people_want == 8572
