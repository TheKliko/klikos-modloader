import re

from modules.request import RobloxApi
from modules import request


class DeployHistory:
    ROBLOX_PLAYER: list[dict[str, str]] = []
    ROBLOX_STUDIO: list[dict[str, str]] = []
    ALL: list[dict[str, str]] = []


    def __init__(self) -> None:
        url: str = RobloxApi.deploy_history()
        response = request.get(url)
        deploy_history: list[str] = reversed(response.text.splitlines())

        for line in deploy_history:
            if line.startswith('New WindowsPlayer'):
                version_match: re.Match | None = re.search(r'version-\w+', line)
                git_hash_match: re.Match | None = re.search(r'git hash: ([\w.]+)', line)
                if version_match is None or git_hash_match is None:
                    continue

                version: str = version_match.group(0)
                git_hash: str = git_hash_match.group(1)
                if git_hash == ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'):
                    continue

                data: dict[str, str] = {
                    'version': version,
                    'git_hash': git_hash
                }
                if data not in self.ROBLOX_PLAYER:
                    self.ROBLOX_PLAYER.append(data)

            elif line.startswith('New Studio64'):
                version_match: re.Match | None = re.search(r'version-\w+', line)
                git_hash_match: re.Match | None = re.search(r'git hash: ([\w.]+)', line)
                if version_match is None or git_hash_match is None:
                    continue

                version: str = version_match.group(0)
                git_hash: str = git_hash_match.group(1)
                if git_hash == ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'):
                    continue

                data: dict[str, str] = {
                    'version': version,
                    'git_hash': git_hash
                }
                if data not in self.ROBLOX_STUDIO:
                    self.ROBLOX_STUDIO.append(data)
            
            else:
                continue

            if data not in self.ALL:
                self.ALL.append(data)


deploy_history: DeployHistory = DeployHistory()


def get() -> DeployHistory:
    return deploy_history