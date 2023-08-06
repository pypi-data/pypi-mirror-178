from ..domain.match import Match
from ..constants import constants
import requests
from urllib.parse import urljoin
import json
from typing import List

def get_all_matches() -> List[Match]:
    url = urljoin(constants.URL_API_BASE, constants.ENDPOINT_ALL_MATCHES)
    response = requests.get(url)
    
    return [ Match.from_json(match_json) for match_json in response.json() ]

def main():
    result = get_all_matches()

if __name__ == '__main__':
    main()

