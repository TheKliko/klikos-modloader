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
    for filepath in directory.iterdir():
        if filepath.is_file() and filepath.name not in required_file_hashes:
            filepath.unlink()

    return missing_file_hashes