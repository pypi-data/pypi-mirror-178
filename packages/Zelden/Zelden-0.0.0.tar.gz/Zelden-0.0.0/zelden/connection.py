from requests import Session
from consts import url, headers
from credentials import api_key
from params import set_json
from rest_connection import RESTConnection


class Connection(RESTConnection):
    def __int__(self, *args, ):
        pass

    def get(self):
        pass

    def _connection(self, start: int, end: int, amount: int, replacement: bool):
        content = set_json(api_key=api_key, start=start, end=end, amount=amount, replacement=replacement)
        s = Session()
        response = s.post(url=url, json=content, headers=headers)
        return response.json()
