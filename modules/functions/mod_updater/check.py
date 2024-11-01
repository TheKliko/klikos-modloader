import os
import json
from typing import Literal

from modules.functions.mod_updater import versions


def check_for_mod_updates(mods: list[str], latest_version: str) -> dict|Literal[False]:
    if not mods:
        return False
    

    mods_to_check: list[str] = []
    for mod in mods:
        if os.path.isfile(os.path.join(mod, "info.json")):
            mods_to_check.append(mod)
    
    if not mods_to_check:
        return False
    
    latest_version_hash: str = versions.get_git_hash(version=latest_version)
    
    outdated_mods: dict[str,list[str]] = {}
    for mod in mods_to_check:
        try:
            with open(os.path.join(mod, "info.json"), "r") as file:
                data: dict = json.load(file)
                mod_version: str = data.get("clientVersionUpload", None)
                git_hash: str = versions.get_git_hash(version=mod_version)
                if git_hash != latest_version_hash:

                    if git_hash not in outdated_mods:
                        outdated_mods[git_hash] = []
                    outdated_mods[git_hash].append(mod)

        except:
            continue
    
    if not outdated_mods:
        return False
    
    return outdated_mods