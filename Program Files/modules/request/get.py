import logging
import requests

from .exceptions import RequestError


def get(url: str, attemps: int = 3) -> requests.Response:
    try:
        if attemps < 0:
            logging.error("GET request failed: "+url)
            raise RequestError("GET request failed: "+url)

        logging.info("Attempting GET request: "+url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response

        except Exception as e:
            logging.warning("GET request failed! "+type(e).__name__+": "+str(e))
            get(url, attemps-1)

    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))