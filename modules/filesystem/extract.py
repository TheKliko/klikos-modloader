import os
from zipfile import ZipFile
from pathlib import Path

from modules import Logger

from .exceptions import FileExtractError

from py7zr import SevenZipFile


def extract(source: str | Path, destination: str | Path) -> None:
    source = Path(source)
    destination = Path(destination)

    Logger.info(f"Extracting file: {source.name}...")

    if not os.access(destination.parent, os.W_OK):
        raise FileExtractError(f"Write permissions denied for {destination.parent}")

    os.makedirs(destination.parent, exist_ok=True)

    match source.suffix:
        case ".zip":
            with ZipFile(source, "r") as archive:
                archive.extractall(destination)

        case ".7z":
            with SevenZipFile(source, "r") as archive:
                archive.extractall(destination)

        case _:
            raise FileExtractError(f"Unsupported file format: {source.name}")