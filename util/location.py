from functools import lru_cache

import requests
import geopy.distance

# Code taken from https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
@lru_cache(maxsize=None)
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

@lru_cache(maxsize=None)
def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "longitude": response.get("longitude"),
        "latitude": response.get("latitude")
    }
    return location_data


def get_distance(coords_1, coords_2):
    return geopy.distance.geodesic(coords_1, coords_2).km


earth_circumference_km = 40075
max_distance_on_earth = earth_circumference_km / 2