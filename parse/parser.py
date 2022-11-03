"""A module that contains logic for parsing HTML pages from Atlas Obscura"""
from bs4 import BeautifulSoup

import unicodedata

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
    lat: float
    long: float
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

        self.name = parser.find("h1", class_="DDPage__header-title").text
        self.num_people_visited = int(parser.find_all("div", class_="title-md item-action-count")[0].text) # should use more precise class
        self.num_people_want = int(parser.find_all("div", class_="title-md item-action-count")[1].text)
        self.short_desc = parser.find("h3", class_="DDPage__header-dek").text.strip()
        self.place_tags = list(map(lambda anchor : anchor.text.strip(), parser.find_all("a", class_="itemTags__link")))

        # The description is in multiple <p> elements. We need to find them all, strip whitespace characters and join them back
        desc_parts = list(map(lambda p : p.text.strip(), parser.find("div", {"id": "place-body"}).find_all("p")))
        desc_parts = list(filter(lambda desc : bool(desc), desc_parts))
        self.desc = ' '.join(desc_parts)

        self.nearby = list(map(lambda near : near.text.strip(), parser.find_all('div', class_='DDPageSiderailRecirc__item-title')))

        # The address is written across multiple lines, so we need to remove the white space and join them to have a single line.
        address_parts = list(filter(lambda address_part : bool(address_part.text.strip()), parser.find('address').find("div").contents))
        self.address = ', '.join(map(lambda address_part : address_part.text.strip(), address_parts))

        coordinates = parser.find('div', class_='DDPageSiderail__coordinates').text.strip().split(sep=',')
        self.lat, self.long = tuple(map(float, coordinates))


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