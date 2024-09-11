import logging

from modules.other.api import RobloxApi
from modules.utils import request

from .exceptions import LatestVersionNotFoundError


def latest(binary_type: str, channel: str = 'live') -> str:
    try:
        url: str = RobloxApi.latest_version(channel=channel, binary_type=binary_type)

        response = request.get(url)
        data: dict = response.json()
        version: str = data['clientVersionUpload']

        return version

    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise LatestVersionNotFoundError(f'[{type(e).__name__}] {str(e)}')