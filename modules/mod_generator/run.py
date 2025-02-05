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
from .generate_user_selected_files import generate_user_selected_files
from .add_watermark import add_watermark


def run(name: str, color1, color2, angle: int, output_dir: str | Path, user_selected_files: list[dict[str, Path | list[str]]] | None = None) -> None:
    Logger.info("Generating mod...", prefix="mod_generator.run()")
    output_dir = Path(output_dir)
    output_target: Path = output_dir / name

    if output_target.exists():
        raise FileExistsError("Cannot generate a mod that already exists!")

    deployment: Deployment = Deployment("Studio")

    with TemporaryDirectory(prefix=f"mod_generator_") as tmp:
        temporary_directory: Path = Path(tmp)
        temp_target: Path = temporary_directory / name
        temp_target.mkdir(parents=True, exist_ok=True)

        Logger.info("Writing info.json...", prefix="mod_generator.run()")
        data: dict = {"clientVersionUpload": deployment.version, "watermark": "Generated with Kliko's mod generator"}
        with open(temp_target / "info.json", "w") as file:
            json.dump(data, file, indent=4)

        Logger.info("Downloading LuaPackages...", prefix="mod_generator.run()")
        download_luapackages(deployment.version, temporary_directory)

        Logger.info("Locating ImageSets...", prefix="mod_generator.run()")
        imageset_path: Path = locate_imagesets(temporary_directory / deployment.version)
        shutil.copytree((temporary_directory / deployment.version / imageset_path), (temp_target / imageset_path), dirs_exist_ok=True)
        
        Logger.info("Locating ImageSetData...", prefix="mod_generator.run()")
        imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / deployment.version)
        
        Logger.info("Getting icon map...", prefix="mod_generator.run()")
        icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / deployment.version / imagesetdata_path)

        Logger.info("Generating modded ImageSets...", prefix="mod_generator.run()")
        generate_imagesets((temp_target / imageset_path), icon_map, color1, color2, angle)

        Logger.info("Generating additional files...", prefix="mod_generator.run()")
        generate_additional_files(temp_target, color1, color2, angle)

        if user_selected_files:
            Logger.info("Generating user selected files...", prefix="mod_generator.run()")
            generate_user_selected_files(temp_target, color1, color2, angle, user_selected_files)

        Logger.info("Adding watermark...", prefix="mod_generator.run()")
        add_watermark((temp_target / imageset_path))

        if output_target.exists():
            raise FileExistsError("Cannot generate a mod that already exists!")

        Logger.info("Copying files...", prefix="mod_generator.run()")
        os.rename(temp_target, output_target)

    Logger.info("Done!", prefix="mod_generator.run()")