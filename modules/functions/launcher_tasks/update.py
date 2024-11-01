import threading
from typing import Literal

from modules.logger import logger
from modules import request
from modules.request import RobloxApi, GitHubApi, Response
from modules.filesystem import Directory, download, extract


def update(latest_version: str) -> None:
    logger.info(f"Downloading Roblox version: {latest_version}")


    logger.info("Getting filemap...")
    response: Response = request.get(GitHubApi.filemap())
    filemap: dict = response.json()

    common_filemap: dict = filemap.get("common", {})
    player_filemap: dict = filemap.get("player", {})
    studio_filemap: dict = filemap.get("studio", {})

    logger.info("Getting package manifest...")
    # . . .
    raise NotImplementedError("NOT IMPLEMENTED!")

    logger.info("Downloading files...")
    # Download each file simultaneously using threading.Thread


def worker() -> None:
    pass