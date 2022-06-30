import requests

from Pokemons.settings import POKE_URL

ENDPOINTS = [
    "pokemon",
]


def validate(endpoint):
    if endpoint not in ENDPOINTS:
        raise ValueError("Unknown API endpoint '{}'".format(endpoint))
    return None


def api_url_build(endpoint, subresource=None):
    validate(endpoint)
    if subresource is not None:
        return "/".join([POKE_URL, endpoint, subresource, ""])
    return "/".join([POKE_URL, endpoint, ""])


def _call_api(endpoint, subresource=None):
    url = api_url_build(endpoint, subresource)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def get_data(endpoint, resource_id=None):
    data = _call_api(endpoint, resource_id)
    return data


def get_data(endpoint, subresource=None, **kwargs):
    data = _call_api(endpoint, subresource)
    return data

