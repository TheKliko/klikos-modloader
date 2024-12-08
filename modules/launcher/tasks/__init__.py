from typing import Literal, Callable
import json

from modules import Logger

from ..deployment_info import Deployment
from .check_downloaded_files import check_downloaded_files
from .download_missing_files import download_missing_files
from .restore_default_files import restore_default_files

from customtkinter import StringVar


def run(mode: Literal["Player", "Studio"], textvariable: StringVar, end_signal: Callable) -> None:
    Logger.info("Getting deployment info...")
    deployment: Deployment = Deployment(mode)
    textvariable.set(f"{deployment.version.capitalize()} ({deployment.channel})")

    Logger.info("Checking Downloads folder...")
    missing_file_hashes: list[str] = check_downloaded_files(deployment, mode)

    # TODO: CHECK IF ROBLOX IS RUNNING
    # ASK IF USER WANTS TO CONTINUE IF IT IS

    # FORCE CLOSE ROBLOX

    if missing_file_hashes:
        Logger.info("Downloading missing files...")
        textvariable.set("Updating Roblox...")
        download_missing_files(deployment, mode, missing_file_hashes)
    
    Logger.info("Restoring default files...")
    textvariable.set("Installing Roblox...")
    restore_default_files(deployment, mode)
    
    # print(deployment.manifest_version)
    # for item in deployment.package_manifest:
    #     print(json.dumps(item, indent=4))

    end_signal()