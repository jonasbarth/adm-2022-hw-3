"""Tests for the parser module"""
import codecs

from parse import PlaceParser


def test_name_is_parsed():
    with codecs.open("./resources/City Hall Station – New York, New York - Atlas Obscura.html", "r", "utf-8") as file:
        html = file.read()
        parser = PlaceParser(html)

        parser.parse()

        assert parser.name == "City Hall Station"


def test_num_people_visited_is_parsed():
    with codecs.open("./resources/City Hall Station – New York, New York - Atlas Obscura.html", "r", "utf-8") as file:
        html = file.read()
        parser = PlaceParser(html)

        parser.parse()

        assert parser.num_people_visited == 1826



