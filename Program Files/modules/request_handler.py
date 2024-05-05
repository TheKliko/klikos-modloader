import os
import logging

from packages import requests


def request_json(source: str) -> dict | None:
    logging.info(f'Getting json data from {source}')
    try:
        response = requests.get(source)
        config = response.json()
        return config
    
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()