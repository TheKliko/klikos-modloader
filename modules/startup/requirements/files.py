import sys
from pathlib import Path
import json

from modules import Logger
from modules.filesystem import File, restore_from_meipass, Directory


IS_FROZEN: bool = getattr(sys, "frozen", False)


def check_required_files() -> None:
    missing_files: list[str] = []

    for file in File.REQUIRED_FILES:
        file_exists: bool = file.is_file()

        if file_exists and not IS_FROZEN:
            continue

        elif not file_exists and not IS_FROZEN:
            missing_files.append(file.name)

        elif not file_exists and IS_FROZEN:
            restore_from_meipass(file)

        elif file_exists and IS_FROZEN:
            check_file_content(file)
    
    if missing_files != []:
        raise Exception(f"The following files are missing: {', '.join(missing_files)}")


def check_file_content(file: Path) -> None:
    root: Path = Directory.ROOT
    relative_path: Path = file.relative_to(root)

    MEIPASS: Path = Path(sys._MEIPASS)
    backup: Path = MEIPASS / relative_path

    if not file.is_file():
        restore_from_meipass(file)
        return
    
    try:
        with open(file, "r") as current_file:
            current_data: dict = json.load(current_file)
        
        with open(backup, "r") as backup_file:
            backup_data: dict = json.load(backup_file)

        filtered_data: dict = backup_data.copy()
        for key in filtered_data:
            if key in current_data:
                if isinstance(current_data[key], dict):
                    if "value" in current_data[key].keys():
                        filtered_data[key]["value"] = current_data[key]["value"]

        if current_data != filtered_data:
            with open(file, "w") as current_file:
                json.dump(filtered_data, current_file, indent=4)

    except Exception as e:
        Logger.warning(f"Failed to verify content of {file.name}! {type(e).__name__}: {e}")