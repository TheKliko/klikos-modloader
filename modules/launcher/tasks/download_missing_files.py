from pathlib import Path
from typing import Literal

from modules import Logger
from modules.request import Api
from modules.filesystem import download, Directory

from ..deployment_info import Deployment


def download_missing_files(deployment: Deployment, mode: Literal["Player", "Studio"], missing_file_hashes: list[str]) -> None:
    for item in deployment.package_manifest:
        if item["hash"] not in missing_file_hashes:
            continue

        file: str = item["file"]
        hash: str = item["hash"]
        size: int = item["size"]
        # rawsize: int = item["rawsize"]
        # target: Path = Path(item["target"])

        # size_kb: float = round(size / 1024, 2)
        size_mb: float = round(size / 1048576, 2)
        Logger.info(f"Downloading file: {file} (hash: {hash}, size: {size_mb} MB)")
        download_target: Path = Directory.DOWNLOADS / mode / hash
        download(Api.Roblox.Deployment.download(deployment.version, file), download_target)