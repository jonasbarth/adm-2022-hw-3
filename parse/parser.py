"""A module that contains logic for parsing HTML pages from Atlas Obscura"""
from datetime import datetime

from bs4 import BeautifulSoup

#TODO create a place class to hold all the data
#TODO create a place writer to write to a tsv file
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
    appears_in: []
    related_places: []
    url: str

    parsed = False

    def __init__(self, html):
        self.html = html
        self.parser = BeautifulSoup(self.html, 'html.parser')

    def parse(self):
        """Parses the HTML and extracts data."""
        if self.parsed:
            return

        self.name = self.parser.find("h1", class_="DDPage__header-title").text
        self.num_people_visited = int(
            self.parser.find_all("div", class_="title-md item-action-count")[0].text)  # should use more precise class
        self.num_people_want = int(self.parser.find_all("div", class_="title-md item-action-count")[1].text)
        self.short_desc = self.parser.find("h3", class_="DDPage__header-dek").text.strip()
        self.place_tags = list(
            map(lambda anchor: anchor.text.strip(), self.parser.find_all("a", class_="itemTags__link")))

        # The description is in multiple <p> elements. We need to find them all, strip whitespace characters and join them back
        desc_parts = list(map(lambda p: p.text.strip(), self.parser.find("div", {"id": "place-body"}).find_all("p")))
        desc_parts = list(filter(lambda desc: bool(desc), desc_parts))
        self.desc = ' '.join(desc_parts)

        self.nearby = list(
            map(lambda near: near.text.strip(), self.parser.find_all('div', class_='DDPageSiderailRecirc__item-title')))

        # The address is written across multiple lines, so we need to remove the white space and join them to have a single line.
        address_parts = list(
            filter(lambda address_part: bool(address_part.text.strip()),
                   self.parser.find('address').find("div").contents))
        self.address = ', '.join(map(lambda address_part: address_part.text.strip(), address_parts))

        coordinates = self.parser.find('div', class_='DDPageSiderail__coordinates').text.strip().split(sep=',')
        self.lat, self.long = tuple(map(float, coordinates))

        all_editors = list(map(lambda contributor: contributor.text.strip(),
                               self.parser.find_all('a', class_='DDPContributorsList__contributor')))

        # Some editors have a duplicate first character that is followed by \n, we need to remove this
        duplicate_char_editors = list(map(lambda e: e[1:].strip(), filter(lambda e: '\n' in e, all_editors)))
        normal_editors = list(filter(lambda e: '\n' not in e, all_editors))

        self.editors = normal_editors + duplicate_char_editors

        self.publication_date = datetime.strptime(self.parser.find('div', class_='DDPContributor__name').text,
                                                  '%b %d, %Y')
        self.appears_in = self._find_appears_in_element()
        self.related_places = self._find_related_places()

    def _find_related_places(self):
        return self._find_linked_places('Related')

    def _find_appears_in_element(self):
        return self._find_linked_places('Appears')

    def _find_linked_places(self, title):
        all_divs = self.parser.find_all('div', class_='athanasius')
        div_with_appears_in, = list(filter(lambda div: title in div.text,
                                           filter(lambda div: div.find('div', class_='CardRecircSection__title'),
                                                  all_divs)))

        appears_in_titles = list(map(lambda h3: h3.text.strip(), div_with_appears_in.find_all('h3')))

        return appears_in_titles
