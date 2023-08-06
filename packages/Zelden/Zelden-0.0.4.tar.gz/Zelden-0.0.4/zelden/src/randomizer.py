import os
import requests
from zelden.src.consts import headers, url
from zelden.src.set_json import set_json
from zelden.src.exceptions import RangeException, NotEnoughDataError
from zelden.src.credentials import check_credentials


# TODO: Implement a better SOLID approach to microservice the data handling/distribution


def randrange(start: int = 1, end: int = 10, amount: int = 1, replacement: bool = False):
    domain = abs(end - start) + 1
    if amount > domain and not replacement:
        raise RangeException('Amount is greater than domain. Either set replacement to True or lower amount.')

    if not (start or end or amount):
        raise NotEnoughDataError('One or more arguments are missing')

    apikey = check_credentials()
    s = requests.Session()
    json = set_json(start=start, end=end, amount=amount, replacement=replacement, api_key=apikey)
    response = s.post(url=url, headers=headers, json=json).json()[0]
    result = response.get('result')
    raw_data = result.get('random')
    data = raw_data.get('data')
    return data
