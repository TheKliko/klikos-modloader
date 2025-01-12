import os
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from modules import Logger
from modules.launcher.deployment_info import Deployment

from .download_luapackages import download_luapackages
from .locate_imagesets import locate_imagesets
from .locate_imagesetdata_file import locate_imagesetdata_file
from .get_icon_map import get_icon_map
from .generate_imagesets import generate_imagesets
from .generate_additional_files import generate_additional_files
from .add_watermark import add_watermark


def run(name: str, color1, color2, angle: int, output_dir: str | Path) -> None:
    Logger.info("Generating mod...")
    output_dir = Path(output_dir)
    output_target: Path = output_dir / name

    if output_target.exists():
        raise FileExistsError("Cannot generate a mod that already exists!")

    deployment: Deployment = Deployment("Studio")

    with TemporaryDirectory(prefix=f"mod_generator_") as tmp:
        temporary_directory: Path = Path(tmp)
        temp_target: Path = temporary_directory / name
        temp_target.mkdir(parents=True, exist_ok=True)

        Logger.info("Writing info.json...")
        data: dict = {"clientVersionUpload": deployment.version, "watermark": "Generated with Kliko's mod generator"}
        with open(temp_target / "info.json", "w") as file:
            json.dump(data, file, indent=4)

        Logger.info("Downloading LuaPackages...")
        download_luapackages(deployment.version, temporary_directory)

        Logger.info("Locating ImageSets...")
        imageset_path: Path = locate_imagesets(temporary_directory / deployment.version)
        shutil.copytree((temporary_directory / deployment.version / imageset_path), (temp_target / imageset_path), dirs_exist_ok=True)
        
        Logger.info("Locating ImageSetData...")
        imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / deployment.version)
        
        Logger.info("Getting icon map...")
        icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / deployment.version / imagesetdata_path)

        Logger.info("Generating modded ImageSets...")
        generate_imagesets((temp_target / imageset_path), icon_map, color1, color2, angle)

        Logger.info("Generating additional files...")
        generate_additional_files(temp_target, color1, color2, angle)

        Logger.info("Adding watermark...")
        add_watermark((temp_target / imageset_path))

        if output_target.exists():
            raise FileExistsError("Cannot generate a mod that already exists!")

        Logger.info("Copying files...")
        os.rename(temp_target, output_target)

    Logger.info("Done!")