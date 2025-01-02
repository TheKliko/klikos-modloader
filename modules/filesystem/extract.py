import os
from zipfile import ZipFile
from pathlib import Path

from modules import Logger

from .exceptions import FileExtractError

# from py7zr import SevenZipFile


def extract(source: str | Path, destination: str | Path, ignore_filetype: bool = False) -> None:
    source = Path(source)
    destination = Path(destination)

    Logger.info(f"Extracting file: {source.name}...")

    if destination.is_file():
        raise FileExtractError(f"Destination must be a directory! (destination: {destination.name})")
    if not source.is_file():
        raise FileExtractError(f"Source does not exist! (source: {source.name})")

    destination.parent.mkdir(parents=True, exist_ok=True)
    if not os.access(destination.parent, os.W_OK):
        raise FileExtractError(f"Write permissions denied for {destination.parent}")

    if ignore_filetype:
        with ZipFile(source, "r") as archive:
            archive.extractall(destination)
        return

    match source.suffix:
        case ".zip":
            with ZipFile(source, "r") as archive:
                archive.extractall(destination)

        # case ".7z":
        #     with SevenZipFile(source, "r") as archive:
        #         archive.extractall(destination)

        case _:
            raise FileExtractError(f"Unsupported file format: {source.name}")