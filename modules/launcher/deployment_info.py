from typing import Literal
from pathlib import Path

from modules import request
from modules.request import Api, Response
from modules.filesystem.directories import Directory
from modules.functions.roblox import user_channel


class Deployment:
    channel: str
    version: str
    git_hash: str
    file_version: str

    binaryType: str
    executable_name: str
    base_directory: Path
    executable_path: Path

    manifest_version: str
    package_manifest: list[dict]

    filemap: dict

    app_settings_path: Path
    APP_SETTINGS_CONTENT: str = """<?xml version="1.0" encoding="UTF-8"?>
<Settings>
	<ContentFolder>content</ContentFolder>
	<BaseUrl>http://www.roblox.com</BaseUrl>
</Settings>"""


    def __init__(self, mode: Literal["Player", "Studio"]):
        self.binaryType = f"WindowsStudio64" if mode == "Studio" else f"WindowsPlayer"
        self.executable_name = f"Roblox{mode}Beta.exe"

        self.channel = user_channel.get(self.binaryType)
        self.version, self.git_hash = self._get_version_info(self.binaryType, self.channel)
        self.base_directory = Directory.VERSIONS / self.version
        self.executable_path = self.base_directory / self.executable_name
        self.app_settings_path = self.base_directory / "AppSettings.xml"

        self.filemap = self._get_filemap()
        self.manifest_version, self.package_manifest = self._get_files(self.version)


    def _get_version_info(self, binaryType: str, channel: str) -> tuple[str,str]:
        if channel is None:
            channel = user_channel.get(binaryType)
        response: Response = request.get(Api.Roblox.Deployment.latest(binaryType, channel), cached=True)
        data: dict = response.json()
        return (data["clientVersionUpload"], data["version"])


    def _get_filemap(self) -> dict:
        response: Response = request.get(Api.GitHub.FILEMAP, cached=True)
        data: dict = response.json()
        return data


    def _get_files(self, version: str) -> tuple[str, list[dict]]:
        response: Response = request.get(Api.Roblox.Deployment.manifest(version), cached=True)
        text: str = response.text
        lines: list[str] = text.splitlines()

        manifest_version: str = lines[0]
        if manifest_version != "v0":
            raise Exception(f"Unknown version for rbxPkgManifest: {manifest_version} (expected: v0)")

        del lines[0]

        manifest: list[dict] = [
            {
                "file": lines[i],
                "hash": lines[i+1],
                "size": int(lines[i+2]),
                "rawsize": int(lines[i+3]),
                "target": self._get_target_path(lines[i])
            }
            for i in range(0, len(lines), 4)
        ]

        return (manifest_version, manifest)


    def _get_target_path(self, file: str) -> str:
        for _, files in self.filemap.items():
            if file not in files:
                continue

            extenstion_as_list: list[str] = files[file]
            if not extenstion_as_list:
                return str(self.base_directory)
            
            return str(self.base_directory / Path(*extenstion_as_list))
        
        raise KeyError(f"Could not find key '{file}' in the dictionary!")