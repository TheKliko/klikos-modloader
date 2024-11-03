import os
import json
from copy import deepcopy
import uuid
from typing import Optional

from modules.logger import logger
from modules.filesystem import FilePath, logged_path


FORMAT: dict = {
    "name": "New Integration",
    "id": None,
    "filepath": None,
    "launch_args": None,
    "enabled": False
}


class KeyExistsError(Exception):
    pass


def status(key: str) -> bool:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for integration in data:
        if integration.get("id") == key:
            return integration["enabled"]

    logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")


def create(integration_path: str) -> None:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data: list[dict] = []
    
    else:
        try:
            with open(filepath, "r") as file:
                data = json.load(file)

        except Exception as e:
            logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
            raise

    integration_data = deepcopy(FORMAT)
    integration_data["filepath"] = integration_path
    integration_data["name"] = os.path.basename(integration_path)
    integration_data["id"] = uuid.uuid4().hex

    data.insert(0, integration_data)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def remove(key: str) -> None:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for i, integration in enumerate(data):
        if integration.get("id") == key:
            data.pop(i)
            break
    else:
        logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
    
    if not data:
        try:
            os.remove(filepath)
        except Exception:
            pass


def get(key: str) -> dict:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for integration in data:
        if integration.get("id") == key:
            return integration

    logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")


def get_all() -> list[dict]:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        return []

    try:
        with open(filepath, "r") as file:
            data: list = json.load(file)
        return data

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        return []


def get_active() -> list[tuple[str, Optional[str]]]:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        return []

    try:
        with open(filepath, "r") as file:
            data: list = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        return []
    
    active_apps: list[tuple[str, Optional[str]]] = [
        (app.get("filepath"), app.get("launch_args"))
        for app in data
        if app.get("enabled")
        and app.get("filepath") is not None
    ]
    return active_apps


def set_status(key: str, value: bool) -> None:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for i, integration in enumerate(data):
        if integration.get("id") == key:
            if integration["enabled"] == value:
                return
            data[i]["enabled"] = value
            return

    logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")


def set_name(key: str, value: str) -> None:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for i, integration in enumerate(data):
        if integration.get("id") == key:
            if integration["name"] == value:
                return
            data[i]["name"] = value
            break
    else:
        logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def set_filepath(key: str, value: str) -> None:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for i, integration in enumerate(data):
        if integration.get("id") == key:
            if integration["filepath"] == value:
                return
            data[i]["filepath"] = value
            break
    else:
        logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def set_args(key: str, value: str) -> None:
    filepath: str = FilePath.launch_integrations()
    if not os.path.isfile(filepath):
        logger.error(f"No such file or directory: {logged_path.get(filepath)}")
        raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")

    try:
        with open(filepath, "r") as file:
            data: list[dict] = json.load(file)

    except Exception as e:
        logger.error(f"Failed to read launch_integrations.json, reason: {type(e).__name__}: {e}")
        raise

    for i, integration in enumerate(data):
        if integration.get("id") == key:
            if integration["launch_args"] == value:
                return
            data[i]["launch_args"] = value
            break
    else:
        logger.error(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
        raise KeyError(f"Could not find \"{key}\" in {logged_path.get(filepath)}")
    
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)