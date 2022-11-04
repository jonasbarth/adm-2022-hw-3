"""Module for the Atlas Obscure Place class and related functions."""
from attr import dataclass


@dataclass(frozen=True)
class Place:
    """An immutable class to hold all information related to a place on Atlas Obscura. """
    name: str
    tags: []
    num_people_visited: int
    num_people_want: int
    desc: str
    short_desc: str
    nearby: []
    address: str
    lat: float
    lon: float
    editors: []
    publication_date: any
    appears_in: []
    related_places: []
    url: str


class PlaceBuilder:
    """A builder for the Place class."""
    name: str
    tags: []
    num_people_visited: int
    num_people_want: int
    desc: str
    short_desc: str
    nearby: []
    address: str
    lat: float
    lon: float
    editors: []
    publication_date: any
    appears_in: []
    related_places: []
    url: str


    def set_name(self, name):
        self.name = name
        return self

    def set_tags(self, tags):
        self.tags = tags
        return self

    def set_num_people_visited(self, num_people_visited):
        self.num_people_visited = num_people_visited
        return self

    def set_num_people_want(self, num_people_want):
        self.num_people_want = num_people_want
        return self

    def set_desc(self, desc):
        self.desc = desc
        return self

    def set_short_desc(self, short_desc):
        self.short_desc = short_desc
        return self

    def set_nearby(self, nearby):
        self.nearby = nearby
        return self

    def set_address(self, address):
        self.address = address
        return self

    def set_lat(self, lat):
        self.lat = lat
        return self

    def set_lon(self, lon):
        self.lon = lon
        return self

    def set_editors(self, editors):
        self.editors = editors
        return self

    def set_publication_date(self, publication_date):
        self.publication_date = publication_date
        return self

    def set_appears_in(self, appears_in):
        self.appears_in = appears_in
        return self

    def set_related_places(self, related_places):
        self.related_places = related_places
        return self

    def set_url(self, url):
        self.url = url
        return self

    def build(self):
        return Place(self.name,
                     self.tags,
                     self.num_people_visited,
                     self.num_people_want,
                     self.desc,
                     self.short_desc,
                     self.nearby,
                     self.address,
                     self.lat,
                     self.lon,
                     self.editors,
                     self.publication_date,
                     self.appears_in,
                     self.related_places,
                     self.url)
