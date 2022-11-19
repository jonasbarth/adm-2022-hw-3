"""A module that contains logic for parsing HTML pages from Atlas Obscura"""
import json
import logging
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from domain import PlaceBuilder

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

from joblib import Parallel, delayed


def parse_htmls(htmls, n_jobs=7):
    """Parses a list of html strings using multiprocessing, returning a list of Place objects."""

    def parallel(html):
        try:
            return PlaceParser(html).parse()
        except Exception as e:
            print(f"Problem with parsing {e}, {html}")

    places = Parallel(n_jobs=n_jobs)(delayed(parallel)(html) for html in htmls)
    return places


class PlaceParser:
    """Parses a HTML file of a place in Atlas Obscura."""
    html: str
    url: str

    def __init__(self, html):
        self.html = html
        self.parser = BeautifulSoup(self.html, 'lxml')

    def parse(self):
        """Parses the HTML and extracts data.

        :returns
        a Place object with the data from the HTML.
        """
        meta_data = json.loads(self.parser.find('script', {'type': 'application/ld+json'}).text, strict=False)
        url = meta_data['url']
        name = meta_data['headline']
        num_people_visited = int(
            self.parser.find_all("div", class_="title-md item-action-count")[0].text)  # should use more precise class
        num_people_want = int(self.parser.find_all("div", class_="title-md item-action-count")[1].text)
        short_desc = self.parser.find("h3", class_="DDPage__header-dek").text.strip()
        place_tags = meta_data['keywords'][:-1]

        # The description is in multiple <p> elements. We need to find them all, strip whitespace characters and join them back
        desc_parts = list(map(lambda p: p.text.strip(), self.parser.find("div", {"id": "place-body"}).find_all("p")))
        desc_parts = list(filter(lambda desc: bool(desc), desc_parts))
        desc = ' '.join(desc_parts)

        nearby = list(
            map(lambda near: near.text.strip(), self.parser.find_all('div', class_='DDPageSiderailRecirc__item-title')))

        # The address is written across multiple lines, so we need to remove the white space and join them to have a single line.
        address_parts = list(
            filter(lambda address_part: bool(address_part.text.strip()),
                   self.parser.find('address').find("div").contents))
        address_parts = list(filter(lambda address_part: not isinstance(address_part, Tag), address_parts))
        address = ', '.join(map(lambda address_part: address_part.text.strip(), address_parts))

        lat = self.parser.find('meta', {'property':'og:latitude'})['content']
        lon = self.parser.find('meta', {'property':'og:longitude'})['content']

        all_editors = list(map(lambda contributor: contributor.text.strip(),
                               self.parser.find_all('a', class_='DDPContributorsList__contributor')))

        # Some editors have a duplicate first character that is followed by \n, we need to remove this
        duplicate_char_editors = list(map(lambda e: e[1:].strip(), filter(lambda e: '\n' in e, all_editors)))
        normal_editors = list(filter(lambda e: '\n' not in e, all_editors))

        editors = normal_editors + duplicate_char_editors

        publication_date = datetime.strptime(meta_data['datePublished'], '%Y-%m-%dT%H:%M:%S+00:00')

        appears_in = self._find_appears_in_element()
        related_places = self._find_related_places()

        id = hash((name, lat, lon))

        return PlaceBuilder() \
            .set_name(name) \
            .set_num_people_visited(num_people_visited) \
            .set_num_people_want(num_people_want) \
            .set_short_desc(short_desc) \
            .set_desc(desc) \
            .set_tags(place_tags) \
            .set_nearby(nearby) \
            .set_address(address) \
            .set_lat(lat) \
            .set_lon(lon) \
            .set_editors(editors) \
            .set_publication_date(publication_date) \
            .set_appears_in(appears_in) \
            .set_related_places(related_places) \
            .set_url(url) \
            .set_id(id) \
            .build()

    def _find_related_places(self):
        return self._find_linked_places('Related')

    def _find_appears_in_element(self):
        return self._find_linked_places('Appears')

    def _find_linked_places(self, title):
        all_divs = self.parser.find_all('div', class_='athanasius')
        try:
            div_with_appears_in, = list(filter(lambda div: title in div.text,
                                               filter(lambda div: div.find('div', class_='CardRecircSection__title'),
                                                      all_divs)))
        except ValueError:
            return []

        appears_in_titles = list(map(lambda h3: h3.text.strip(), div_with_appears_in.find_all('h3')))

        return appears_in_titles
