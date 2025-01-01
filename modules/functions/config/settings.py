import os
import sys
import json
from typing import Any

from modules.logger import logger
from modules.filesystem import FilePath, logged_path
from modules.functions.restore_from_mei import restore_from_mei


IS_FROZEN = getattr(sys, "frozen", False)


def value(key: str) -> Any:
    filepath = FilePath.settings()
    if not os.path.isfile(filepath):
        if IS_FROZEN:
            restore_from_mei(filepath)
        else:
            logger.error(f"No such file or directory: {logged_path.get(filepath)}")
            raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")
    
    try:
        with open(filepath, "r") as file:
            data: dict = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    if key not in data:
        logger.error(f"Could not find \"{key}\" in {os.path.basename(filepath)}")
        raise KeyError(f"Failed to find \"{key}\" in {os.path.basename(filepath)}")
    
    if "value" not in data[key]:
        logger.error(f"Could not find value for \"{key}\" in {os.path.basename(filepath)}")
        raise KeyError(f"Failed to read value for \"{key}\" in {os.path.basename(filepath)}")
    
    return data[key]["value"]


def set_value(key: str, value: Any) -> None:
    filepath = FilePath.settings()
    if not os.path.isfile(filepath):
        if IS_FROZEN:
            restore_from_mei(filepath)
        else:
            logger.error(f"No such file or directory: {logged_path.get(filepath)}")
            raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")
    
    try:
        with open(filepath, "r") as file:
            data: dict = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    if key not in data:
        logger.error(f"Could not find \"{key}\" in {os.path.basename(filepath)}")
        raise KeyError(f"Failed to find \"{key}\" in {os.path.basename(filepath)}")
    
    data[key]["value"] = value
    
    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to set value of \"{key}\" in {os.path.basename(filepath)}, reason: {type(e).__name__}: {e}")
        raise
    
    return data[key]["value"]


def get(key: str) -> dict:
    filepath = FilePath.settings()
    if not os.path.isfile(filepath):
        if IS_FROZEN:
            restore_from_mei(filepath)
        else:
            logger.error(f"No such file or directory: {logged_path.get(filepath)}")
            raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")
    
    try:
        with open(filepath, "r") as file:
            data: dict = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    if key not in data:
        logger.error(f"Could not find \"{key}\" in {os.path.basename(filepath)}")
        raise KeyError(f"Failed to find \"{key}\" in {os.path.basename(filepath)}")

    return data[key]


def get_all() -> dict:
    filepath = FilePath.settings()
    if not os.path.isfile(filepath):
        if IS_FROZEN:
            restore_from_mei(filepath)
        else:
            logger.error(f"No such file or directory: {logged_path.get(filepath)}")
            raise FileNotFoundError(f"No such file or directory: {logged_path.get(filepath)}")
    
    try:
        with open(filepath, "r") as file:
            data: dict = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"{type(e).__name__} while reading {os.path.basename(filepath)}: {e}")
        raise

    return data


def restore_all() -> None:
    filepath = FilePath.settings()
    if IS_FROZEN:
        os.remove(filepath)
        restore_from_mei(filepath)
    else:
        logger.error("Failed to restore settings, app is not frozen")
        raise Exception("Failed to restore settings, app is not frozen")