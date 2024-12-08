from typing import Optional

from modules import request
from modules.request import Api, Response


def get(binaryType: str, channel: Optional[str] = None) -> str:
    response: Response = request.get(Api.Roblox.Deployment.latest(binaryType, channel), cached=True)
    data: dict = response.json()
    return data["clientVersionUpload"]