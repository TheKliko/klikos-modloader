from pathlib import Path
import json

from modules import Logger


def apply_custom_font(version_folder_root: Path) -> None:
    Logger.info(f"Applying custom font...")

    new_rbxasset: str = "rbxasset://fonts//CustomFont.ttf"
    custom_font_path: Path = version_folder_root / "content" / "fonts" / "CustomFont.ttf"
    font_families_path: Path = version_folder_root / "content" / "fonts" / "families"

    if not custom_font_path.is_file():
        Logger.warning("CustomFont.ttf does not exist!")
        return
    
    if not font_families_path.is_dir():
        Logger.warning("content/fonts/families not found in version folder!")
        return

    json_files: list[Path] = [
        font_families_path / file for file in font_families_path.iterdir()
        if file.is_file() and file.suffix == ".json"
    ]
    for json_file in json_files:
        with open(json_file, "r") as read_file:
            data: dict = json.load(read_file)

        faces: list[dict] | None = data.get("faces")
        if faces is None:
            continue

        for i, _ in enumerate(faces):
            faces[i]["assetId"] = new_rbxasset
        data["faces"] = faces

        with open(json_file, "w") as write_file:
            json.dump(data, write_file, indent=4)