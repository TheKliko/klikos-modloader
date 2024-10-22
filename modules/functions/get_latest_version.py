from typing import Literal, Optional

from modules.request import RobloxApi, Response
from modules import request
from modules.functions.get_user_channel import get_user_channel


def get_latest_version(binary_type: Literal["WindowsPlayer", "WindowsStudio"], user_channel: Optional[str] = None) -> str:
    if user_channel is None:
        user_channel = get_user_channel(binary_type)
    response: Response = request.get(RobloxApi.latest_version(binary_type, user_channel), cache=True)
    data: dict = response.json()
    return data["clientVersionUpload"]