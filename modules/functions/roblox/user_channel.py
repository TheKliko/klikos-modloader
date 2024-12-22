from modules import request
from modules.request import Api, Response


def get(binaryType: str) -> str:
    response: Response = request.get(Api.Roblox.Deployment.channel(binaryType), cached=True)
    data: dict = response.json()
    return data["channelName"]