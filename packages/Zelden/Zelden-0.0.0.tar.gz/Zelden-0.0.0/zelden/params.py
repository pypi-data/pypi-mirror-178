from typing import Dict, List


def set_json(api_key: str = None, start: int = 1, end: int = 10,
             amount: int = 6, replacement: bool = False) -> List[Dict]:

    content = [{
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": f"{api_key}",
            "n": amount,
            "min": start,
            "max": end,
            "replacement": replacement
        },
        "id": 42
    }]

    return content
