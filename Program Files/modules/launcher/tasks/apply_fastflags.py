import os
import shutil
import json

from modules.filesystem import Directory
from modules.functions import fastflags


def apply_fastflags(version: str) -> None:
    target_directory: str = os.path.join(Directory.versions(), version, "ClientSettings")
    target_file: str = os.path.join(target_directory, "ClientAppSettings.json")
    shutil.rmtree(target_directory, ignore_errors=True)

    all_profiles: list[dict] = fastflags.get()
    active_profiles: list[dict] = [profile["data"] for profile in all_profiles if profile["enabled"] == True]

    if not active_profiles:
        return
    
    combined_data = {}
    for profile in active_profiles:
        combined_data.update(profile)
    
    os.makedirs(target_directory, exist_ok=True)
    with open(target_file, "w") as file:
        json.dump(combined_data, file, indent=4)