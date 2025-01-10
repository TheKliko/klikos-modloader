from typing import Literal
from pathlib import Path
import os

from modules.filesystem import Directory

from ..deployment_info import Deployment


def check_downloaded_files(deployment: Deployment, mode: Literal["Player", "Studio"]) -> list[str]:
    directory: Path = Directory.DOWNLOADS / mode
    directory.mkdir(parents=True, exist_ok=True)

    required_file_hashes: list[str] = [
        item["hash"]
        for item in deployment.package_manifest
    ]
    missing_file_hashes: list[str] = [
        hash for hash in required_file_hashes
        if not directory.joinpath(hash).is_file()
    ]

    # Remove files for older versions
    for file in os.listdir(directory):
        file_as_path = directory / file
        if file_as_path.is_file() and file_as_path.name not in required_file_hashes:
            file_as_path.unlink()

    return missing_file_hashes