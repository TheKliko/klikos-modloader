from modules import request

from modules.functions import user_channel

def get(binary_type: str, channel: str|None = None) -> str:
    channel = channel or user_channel.get(binary_type=binary_type)

    response = request.get(request.RobloxApi.latest_version(binary_type=binary_type, user_channel=channel))
    version: str = response.json()["clientVersionUpload"]

    return version