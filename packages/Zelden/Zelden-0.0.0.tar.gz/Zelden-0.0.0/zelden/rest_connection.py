from abc import ABC
from typing import Tuple


class RESTConnection(ABC):
    def __int__(self, domain: str = None, username: str = None, password: str = None, apikey: str = None,
                url_prefix: str = '/', session_timeout: Tuple[int, int] = None,
                port: int = None, headers: dict = None):

        """
        :param domain: The URL domain of a given API, 'https://rickandmortyapi.com/'
        :param username: For HTTP authentication
        :param password: For HTTP authentication
        :param apikey: Keys generally generated from each individual platform to grant the requester permission
        :param url_prefix: Path/Endpoint path for the API
        :param session_timeout: TBD
        :param port: The leading trail argument attached to the end of an address, e.g. localhost:80
        :param headers:
        """

        # TODO: IMPLEMENT VALIDATIONS
        self.domain = domain
        self.username = username
        self.password = password
        self.apikey = apikey
        self.url_prefix = url_prefix
        self.session_timeout = session_timeout
        self.port = port
        self.headers = headers
        self.url = domain + url_prefix

    def is_reachable(self):
        pass
