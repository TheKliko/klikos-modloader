import os
import json
from copy import deepcopy

from modules.logger import logger
from modules.filesystem import FilePath


FORMAT: dict = {
        "name": None,
        "enabled": False,
        "priority": 0
}


def set_name(key: str, value: str) -> None:
    if key == value:
        return

    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        return

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, mod in enumerate(data):
        if mod.get("name") == key:
            data[i]["name"] = value
            break
    else:
        return

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set name of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise

    if not data:
        try:
            os.remove(filepath)
        except Exception:
            pass


def set_priority(key: str, value: int) -> None:
    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        data: list = [deepcopy(FORMAT)]
        data[0]["name"] = key
        data[0]["priority"] = value

    else:
        try:
            with open(filepath, "r") as file:
                data: list[dict] = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
            raise

        for i, mod in enumerate(data):
            if mod.get("name") == key:
                if data[i]["priority"] == value:
                    return
                data[i]["priority"] = value
                if mod["enabled"] == FORMAT["enabled"] and value == FORMAT["priority"]:
                    data.pop(i)
                break
        else:
            if value == FORMAT["priority"]:
                return
            data.append(deepcopy(FORMAT))
            data[-1]["name"] = key
            data[-1]["priority"] = value

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set priority of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise

    if not data:
        try:
            os.remove(filepath)
        except Exception:
            pass


def set_status(key: str, value: bool) -> None:
    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        data: list = [deepcopy(FORMAT)]
        data[0]["name"] = key
        data[0]["enabled"] = value

    else:
        try:
            with open(filepath, "r") as file:
                data: list[dict] = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
            raise

        for i, mod in enumerate(data):
            if mod.get("name") == key:
                if mod["enabled"] == value:
                    return
                data[i]["enabled"] = value
                if value == FORMAT["enabled"] and mod["priority"] == FORMAT["priority"]:
                    data.pop(i)
                break
        else:
            if value == FORMAT["enabled"]:
                return
            data.append(deepcopy(FORMAT))
            data[-1]["name"] = key
            data[-1]["enabled"] = value

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set status of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise

    if not data:
        try:
            os.remove(filepath)
        except Exception:
            pass


def remove(key: str) -> None:
    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        return
    
    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, mod in enumerate(data):
        if mod.get("name") == key:
            data.pop(i)
            break
    else:
        return

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to remove mod \"{key}\" from {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise

    if not data:
        try:
            os.remove(filepath)
        except Exception:
            pass



def get(key: str) -> dict:
    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        data: dict = {}
    
    else:
        try:
            with open(filepath, "r") as file:
                data: list[dict] = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
            raise

    for mod in data:
        if mod.get("name") == key:
            return mod
    else:
        return {}


def get_all() -> list[dict]:
    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        return []
    
    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    return data


def get_active() -> list[str]:
    filepath = FilePath.mods()
    if not os.path.isfile(filepath):
        return []
    
    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    active_mods = [
        mod for mod in data 
        if mod.get("enabled", False) == True and mod.get("name") is not None
    ]
    active_mods.sort(key=lambda mod: mod.get("priority", 0))
    active_mod_names = [mod["name"] for mod in active_mods]

    return active_mod_names