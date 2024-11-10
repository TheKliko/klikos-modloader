from typing import Literal

from modules.request import RobloxApi, Response
from modules import request


def get_user_channel(binary_type: Literal["WindowsPlayer", "WindowsStudio"]) -> str:
    response: Response = request.get(RobloxApi.user_channel(binary_type), cache=True)
    data: dict = response.json()
    return data["channelName"]