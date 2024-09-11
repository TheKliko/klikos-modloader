import logging

from modules.other.api import RobloxApi
from modules.utils import request


class UserChannelNotFoundError(Exception):
    pass


def get(binary_type: str) -> str:
    try:
        url: str = RobloxApi.user_channel(binary_type)
        response = request.get(url)
        data: dict = response.json()
        channel: str = data['channelName']
        return channel
    
    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise UserChannelNotFoundError(f'[{type(e).__name__}] {str(e)}')