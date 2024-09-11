import logging
import requests

from .exceptions import RequestError


def get(url: str, attemps: int = 3) -> requests.Response:
    if attemps < 0:
        logging.error(f'GET request failed: {url}')
        raise RequestError(f'GET request failed: {url}')

    logging.info(f'Attempting GET request: {url}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response

    except Exception as e:
        logging.warning(f'[{type(e).__name__}] {str(e)}')
        get(url, attemps-1)