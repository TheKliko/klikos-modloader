from pathlib import Path

from modules.filesystem import download, extract
from modules.request import Api


def download_luapackages(version: str, output_directory: str | Path) -> None:
    output_directory = Path(output_directory)
    download(Api.Roblox.Deployment.download(version, "extracontent-luapackages.zip"), output_directory / f"{version}-extracontent-luapackages.zip")
    extract(output_directory / f"{version}-extracontent-luapackages.zip", output_directory / version / "ExtraContent" / "LuaPackages")
    (output_directory / f"{version}-extracontent-luapackages.zip").unlink()