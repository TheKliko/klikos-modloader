from typing import Literal
from pathlib import Path
import shutil

from modules import Logger
from modules.filesystem import Directory, extract

from ..deployment_info import Deployment


def restore_default_files(deployment: Deployment, mode: Literal["Player","Studio"]) -> None:
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