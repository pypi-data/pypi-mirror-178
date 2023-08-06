from connection import _connection
from structures import Random


class Zelden:
    class Data(Random):
        pass

    def _parse_raw_data(self, start: int, end: int, amount: int, replacement: bool):
        raw_data = _connection(start=start, end=end, amount=amount, replacement=replacement)



def service_data():
    _parse_raw_data()
