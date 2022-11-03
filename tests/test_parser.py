"""Tests for the parser module"""
import codecs
import datetime

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


def test_short_desc_is_parsed(parser):
    assert parser.short_desc == "A beautiful and abandoned New York subway station from 1904, complete with chandelier."


def test_tags_are_parsed(parser):
    assert parser.place_tags == ['subways', 'subterranean', 'infrastructure', 'subterranean sites', 'abandoned', 'architectural oddities', 'architecture']


def test_desc_is_parsed(parser):
    assert parser.desc == 'The first New York City subway was built and operated by the Interborough Rapid Transit Company (IRT) and opened on October 27, 1904, to the joy of New York elevated train and streetcar riders. The City Hall station on the IRT local track was lavished with fine architectural details, including glass tiles and large chandeliers. However, the Gustavino vaulted ceilings and skylights were lost on busy commuters, and the stop was one of the least-used in the system. It was the only station that did not have turnstiles installed by 1923, and the nearby Brooklyn Bridge stop was frequented by the express train and closer to connecting streetcars. Because of the curved platform, cars with center doors could not be used at this station unless they had specially modified door controls which allowed just the end doors to be opened. In 1945, the station was closed when platforms along the line were being lengthened to accommodate longer trains, and the number of passengers using this station dwindled to very few. Another factor leading to the decline of the station’s use was the fact that a person boarding the train at City Hall with a station intended destination below City Hall or in Brooklyn would wind up on the uptown platform at the Brooklyn Bridge station. They would then have to go upstairs and down to the downtown platform to continue their journey. It was much easier to walk the short distance at street level to the Brooklyn Bridge station. Up until the late 1990’s the passengers on the Lexington Avenue Local (today’s 6 train) had to disembark from the train at the Brooklyn Bridge stop. That is no longer the case. The skylights have been reopened, and the station lights turned back on. While passengers can not get out of the train and experience the City Hall Station as they once might have, they can stay on the train as it loops around on those tracks and heads back north. The New York City Transit Museum hosts periodic tours of the abandoned station; however, you must be a member of the museum to attend. Check the website for details.'


def test_nearby_is_parsed(parser):
    assert parser.nearby == ['African Burial Ground National Monument', 'Tunnel Number 3', 'The Sugar House Prison Window']


def test_address_is_parsed(parser):
    assert parser.address == '31 Centre St, New York, New York, 10007, United States'


def test_coordinates_are_parsed(parser):
    assert parser.lat == 40.7134
    assert parser.long == -74.0046


def test_editors_are_parsed(parser):
    assert parser.editors == ['Rebekah Otto',
                              'Habicurious',
                              'charding407',
                              'Annetta Black',
                              'offtrackplanet',
                              'Seth Teicher',
                              'erjeffery',
                              'Habicurious',
                              'Seth Teicher',
                              'wythe',
                              'Annetta Black',
                              'littlebrumble',
                              'charding407',
                              'fosterc827',
                              'Mike H',
                              'Allan',
                              'jrc2692',
                              'offtrackplanet',
                              'mbison']


def test_pub_date_is_parsed(parser):
    assert parser.publication_date == datetime.datetime(2010, 5, 8)


def test_appears_in(parser):
    assert parser.appears_in == ['30 Unexpected Places to Have a Joyful Adventure in New York City',
                                 '10 Secrets of the New York City Subway',
                                 'The World\'s Top 100 Wonders in 2018',
                                 'New York\'s Top 18 Wonders of 2018',
                                 'New York City History, Hidden In Plain Sight']


def test_related_places(parser):
    assert parser.related_places == ['Crystal Palace Subway',
                                     'Moscow Metro Stations',
                                     'Rove Tunnel',
                                     'Klafthmonos Square Parking Structure Fortification Walls']