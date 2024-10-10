from modules import request


DEFAULT: str = "LIVE"


def get(binary_type: str) -> str:
    response = request.get(request.RobloxApi.user_channel(binary_type=binary_type))
    channel: str = response.json().get("channelName", DEFAULT)
    return channel