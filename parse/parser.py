"""A module that contains logic for parsing HTML pages from Atlas Obscura"""
from bs4 import BeautifulSoup

class PlaceParser:
    """Parses a HTML file of a place in Atlas Obscura."""
    html: str
    name: str
    tags: []
    num_people_visited: int
    num_people_want: int
    desc: str
    short_desc: str
    nearby: []
    address: str
    alt: int
    long: int
    editors: []
    publication_date: any
    related: []
    related_places: []
    url: str

    parsed = False

    def __init__(self, html):
        self.html = html

    def parse(self):
        """Parses the HTML and extracts data."""
        if self.parsed:
            return

        parser = BeautifulSoup(self.html, 'html.parser')

        self.name = parser.find_all("h1")[0].text
        self.num_people_visited = int(parser.find_all("div", class_="title-md item-action-count")[0].text) # should use more precise class





"""
Place Name (to save as placeName): String.
Place Tags (to save as placeTags): List of Strings.
number of people who have been there (to save as numPeopleVisited): Integer.
number of people who want to visit the place(to save as numPeopleWant): Integer.
Description (to save as placeDesc): String. Everything from under the first image up to "know before you go" (orange frame on the example image).
Short Description (to save as placeShortDesc): String. Everything from the title and location up to the image (blue frame on the example image).
Nearby Places (to save as placeNearby): Extract the names of all nearby places, but only keep unique values: List of Strings.
Address of the place(to save as placeAddress): String.
Altitude and Longitude of the place's location(to save as placeAlt and placeLong): Integers
The username of the post editors (to save as placeEditors): List of Strings.
Post publishing date (to save as placePubDate): datetime.
The names of the lists that the place was included in (to save as placeRelatedLists): List of Strings.
The names of the related places (to save as placeRelatedPlaces): List of Strings.
The URL of the page of the place (to save as placeURL):String
"""