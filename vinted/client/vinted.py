"""A simple Vinted API"""

import requests
from requests import Response


class Vinted:
    """An API wrapper for Vinted"""
    BASE_URL_API = "https://www.vinted.fr/api/v2/"
    BASE_URL = "https://www.vinted.fr"

    def __init__(self):
        # Use headers and users agent to be not detected as bot
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0', # noqa
            'sec-fetch-dest': 'none',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'accept-language': 'fr-FR'
        }

        # Create requests Session
        self.session = requests.Session()
        # Send a http requests to get cookies
        self.session.get(self.BASE_URL)

    def get(self, endpoint: str, *args, **kwargs) -> Response:
        headers = {**self.base_headers, **kwargs.get("headers", {})}
        kwargs['headers'] = headers
        return self.session.get(
            self.BASE_URL_API + endpoint,
            *args,
            **kwargs
        )
