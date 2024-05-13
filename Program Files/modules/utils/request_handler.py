"""# request_handler.py

request_handler.py is a module used in Kliko's modloader,
it's purpose is to handle requests made with the Requests HTTP Library
"""


import logging
import os
from typing import Any

from packages import requests


class URLNotGivenError(Exception):
    """Exception raised when attempting to make a get request without providing a URL"""
    pass


class OutOfAttemptsError(Exception):
    """Exception raised when attempting to make a get request has failed too many times"""
    pass


class RequestJSONKeyError(Exception):
    """Exception raised when a KeyError occurs while requesting a json value"""
    pass


def request(url: str, request_type: str = 'json', attempts: int = 3, json_key: str = '') -> Any:
    """Function called to make a get request
    
    :param url: the URL that will be requested
    :type url: str
    :param request_type: (optional) the type of request. Default: 'json'
    :type request_type: str
    :param attempts: (optional) the number of times it tries to send a get request before raising an error. Default: 3
    :type attempts: int
    :param json_key: (optional) the key to extract from the JSON response. Only required if request_type is 'json_value'.
    :type json_key: str
    :rtype Any
    :return The returned value of the get request if successful, otherwise None
    """

    logging.info(f'Attempting request with url: {url}')
    try:
        
        if url is None:
            raise URLNotGivenError('No URL was given.')

        if request_type == 'json':
            response = requests.get(url)
            response.raise_for_status()
            config = response.json()
            logging.info('Request successful')
            return config
        
        elif request_type == 'json_value':
            if not json_key:
                raise RequestJSONKeyError('No key was given.')
            
            response = requests.get(url)
            response.raise_for_status()
            config = response.json()
            try:
                value = config[json_key]
            except KeyError:
                raise RequestJSONKeyError(f'Could not find key "{json_key}" in the response')
            logging.info('Request successful')
            return value

        elif request_type == 'text':
            response = requests.get(url)
            response.raise_for_status()
            text = response.text
            logging.info('Request successful')
            return text
    
    except URLNotGivenError as e:
        logging.error(f'An {type(e).__name__} occured: {str(e)}')
    
    except requests.Timeout as e:
        logging.error(f'A {type(e).__name__} occured: {str(e)}')
    
    except requests.ConnectionError as e:
        logging.error(f'A {type(e).__name__} occured: {str(e)}')
        if attempts > 0:
            logging.debug('Retrying...')
            return request(request_type=request_type, url=url, attempts=attempts-1)
        else:
            logging.warning('Too many attempts. Returning None')

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    
    logging.warning('Request failed.')
    return None


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()