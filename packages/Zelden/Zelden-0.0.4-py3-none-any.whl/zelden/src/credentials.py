import os
from zelden.src.exceptions import CredentialsError


def credentials(apikey: str = None):
    os.environ['APIKEY'] = apikey


def check_credentials():
    apikey: str = os.getenv('APIKEY')
    if not apikey:
        raise CredentialsError('No credentials found. Set it with set_credentials function')
    return apikey
