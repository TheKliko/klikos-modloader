from typing import Literal
from pathlib import Path
import shutil

from modules import Logger
from modules.filesystem import Directory, extract

from ..deployment_info import Deployment


def restore_default_files(deployment: Deployment, mode: Literal["Player","Studio"]) -> None:
    # Remove older and current version(s)
    if Directory.VERSIONS.is_dir():
        for directory in Directory.VERSIONS.iterdir():

            if not directory.is_dir():
                continue

            executable_path: Path = directory / deployment.executable_name
            eurotrucks_path: Path = directory / "eurotrucks2.exe"
            if executable_path.is_file():
                Logger.info(f"Removing directory: {directory}...")
                shutil.rmtree(directory, ignore_errors=True)
            
            if mode == "Player" and eurotrucks_path.is_file():
                Logger.info(f"Removing directory: {directory}...")
                shutil.rmtree(directory, ignore_errors=True)

    # Restore files for current version
    for item in deployment.package_manifest:
        file: str = item["file"]
        hash: str = item["hash"]
        # size: int = item["size"]
        # rawsize: int = item["rawsize"]
        target: Path = Path(item["target"])

        source: Path = Directory.DOWNLOADS / mode / hash

        target.mkdir(parents=True, exist_ok=True)
        if file.endswith(".zip"):
            extract(source, target, ignore_filetype=True)
        else:
            shutil.copy(source, target)

    # Add AppSettings.xml
    Logger.info("Writing AppSettings.xml")
    deployment.app_settings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(deployment.app_settings_path, "w") as appsettings:
        appsettings.write(deployment.APP_SETTINGS_CONTENT)