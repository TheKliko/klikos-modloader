import logging
import os
import requests

from typing import Any


class RequestError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


class RequestKeyError(Exception):
    f"""Exception raised by {os.path.basename(__file__)} when a KeyError occurs"""
    pass


class RequestType:
    JSON: str = 'json'
    JSON_VALUE: str = 'json_value'
    TEXT: str = 'text'


def request(url: str, request_type: str = RequestType.JSON, json_key: str = None, attempts: int = 3) -> Any:
    """
    Make a get request
    
    :param url: the URL that will be requested
    :param request_type: (optional) the type of request. Default: 'json'
    :param attempts: (optional) the number of times it tries to send a get request before raising an error. Default: 3
    :param json_key: (optional) the key to extract from the JSON response. Only required if request_type is 'json_value'.
    
    :type url: str
    :type request_type: str
    :type attempts: int
    :type json_key: str

    :rtype Any
    :return The returned value of the get request if successful, otherwise None
    """

    logging.info(f'Attempting {request_type}-request at {url}')
    try:
        
        if url is None:
            raise RequestError('No URL was given')

        if request_type == RequestType.JSON:
            response = requests.get(url)
            response.raise_for_status()

            config: dict = response.json()

            logging.info('Request successful')
            return config
        
        elif request_type == RequestType.JSON_VALUE:
            if not json_key:
                raise RequestKeyError('No key was given.')
            
            response = requests.get(url)
            response.raise_for_status()

            config: dict = response.json()

            if not json_key in config.keys():
                raise RequestKeyError(f'Could not find key "{json_key}" in the response')

            value = config[json_key]

            logging.info('Request successful')
            return value

        elif request_type == RequestType.TEXT:
            response = requests.get(url)
            response.raise_for_status()

            text = response.text

            logging.info('Request successful')
            return text
        
        else:
            raise RequestError('Invalid request type')
    
    except requests.Timeout as e:
        raise RequestError('Request timed out')
    
    except requests.ConnectionError as e:
        logging.error(f'A {type(e).__name__} occured: {str(e)}')
        if attempts > 0:
            logging.debug('Retrying...')
            return request(request_type=request_type, url=url, attempts=attempts-1)
        else:
            raise RequestError('Too many attempts')

    except Exception as e:
        raise RequestError(f'An unexpected {type(e).__name__} occured: {str(e)}')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()