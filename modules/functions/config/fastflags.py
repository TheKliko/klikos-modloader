import os
import json
from copy import deepcopy

from modules.logger import logger
from modules.filesystem import FilePath, logged_path


FORMAT: dict = {
        "name": None,
        "description": None,
        "enabled": False,
        "data": {}
}


class KeyExistsError(Exception):
    pass


def set_name(key: str, value: str) -> None:
    if key == value:
        return

    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, profile in enumerate(data):
        if profile.get("name") == value:
            logger.error(f"KeyExistsError: Another profile with the same name already exists")
            raise KeyExistsError("Another profile with the same name already exists")

    for i, profile in enumerate(data):
        if profile.get("name") == key:
            data[i]["name"] = value
            break
    else:
        logger.error(f"KeyError: Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")

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


def set_status(key: str, value: bool) -> None:
    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        logger.error(f"FileNotFoundError: No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, profile in enumerate(data):
        if profile.get("name") == key:
            if profile["enabled"] == value:
                return
            data[i]["enabled"] = value
            break
    else:
        logger.error(f"KeyError: Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set status of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise


def set_description(key: str, value: str | None) -> None:
    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        logger.error(f"FileNotFoundError: No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")
    
    if not value:
        value = None

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, profile in enumerate(data):
        if profile.get("name") == key:
            data[i]["description"] = value
            break
    else:
        logger.error(f"KeyError: Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set description of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise


def set_data(key: str, value: dict) -> None:
    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        logger.error(f"FileNotFoundError: No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, profile in enumerate(data):
        if profile.get("name") == key:
            data[i]["data"] = value
            break
    else:
        logger.error(f"KeyError: Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set data of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise


def create(key: str, description: str | None, fastflags: dict | None) -> None:
    profile: dict = deepcopy(FORMAT)
    profile["name"] = key
    profile["description"] = description
    if fastflags:
        profile["data"] = fastflags

    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        data: list[dict] = [profile]

    else:
        try:
            with open(filepath, "r") as file:
                data: list[dict] = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
            raise

        for i, existing_profile in enumerate(data):
            if existing_profile.get("name") == key:
                logger.error(f"KeyExistsError: Another profile with the same name already exists")
                raise KeyExistsError("Another profile with the same name already exists")
        else:
            data.insert(0, profile)

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to create profile \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise


def remove(key: str) -> None:
    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        logger.error(f"FileNotFoundError: No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    for i, profile in enumerate(data):
        if profile.get("name") == key:
            data.pop(i)
            break
    else:
        return

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to remove key \"{key}\" from {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise

    if not data:
        try:
            os.remove(filepath)
        except Exception:
            pass



def get(key: str) -> dict:
    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        data: dict = {}
    
    else:
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
            raise

    for profile in data:
        if profile.get("name") == key:
            return profile
    else:
        return {}


def get_all() -> list[dict]:
    filepath = FilePath.fastflags()
    if not os.path.isfile(filepath):
        return []
    
    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    return data