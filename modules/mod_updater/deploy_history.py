from modules import request
from modules.request import Response, Api

from .exceptions import DeployHistoryError


class Deployment:
    version: str
    hash: str
    binaryType: str


    def __init__(self, binaryType: str, version: str, hash: str):
        self.binaryType = binaryType
        self.version = version
        self.hash = hash


class DeployHistory:
    class LatestVersion:
        player: str
        studio: str

    player: list[Deployment]
    studio: list[Deployment]
    mixed: list[Deployment]


    def __init__(self, latest_version: str) -> None:
        self.player, self.studio, self.mixed = self._get_history()

        if self.is_player_version(latest_version):
            self.LatestVersion.player = latest_version
            self.LatestVersion.studio = self.studio_equivalent(latest_version)
        elif self.is_studio_version(latest_version):
            self.LatestVersion.studio = latest_version
            self.LatestVersion.player = self.player_equivalent(latest_version)
    

    def _get_history(self) -> tuple[list[Deployment], list[Deployment], list[Deployment]]:
        response: Response = request.get(Api.Roblox.Deployment.HISTORY)
        text: str = response.text
        lines: list[str] = text.splitlines()

        player: list[Deployment] = []
        studio: list[Deployment] = []
        mixed: list[Deployment] = []

        for entry in lines:
            try:
                items: list[str] = entry.removeprefix("New ").removesuffix(" ...").split()
                binary_type: str = items[0]
                if binary_type == "Studio64":
                    binary_type = "WindowsStudio64"
                version: str = items[1]
                hash: str = items[-1]

                deployment: Deployment = Deployment(binary_type, version, hash)

                if binary_type == "WindowsPlayer":
                    player.insert(0, deployment)
                elif binary_type == "WindowsStudio64":
                    studio.insert(0, deployment)
                
                mixed.insert(0, deployment)

            except Exception:
                continue

        return (player, studio, mixed)


    def get_hash(self, version: str) -> str:
        for deployment in self.mixed:
            if deployment.version == version:
                return deployment.hash
        raise DeployHistoryError(f"Could not get hash of {version}")


    def get_studio_version(self, hash: str) -> str:
        for deployment in self.mixed:
            if deployment.hash == hash:
                return deployment.version
        raise DeployHistoryError(f"Could not get version of {hash}")


    def player_equivalent(self, version: str) -> str:
        for deployment in self.studio:
            if deployment.version == version:
                studio_hash = deployment.hash
                break
        else:
            raise DeployHistoryError(f"Could not find WindowsPlayer equivalent of {version}! Given version is not WindowsStudio64")
        
        for deployment in self.player:
            if deployment.hash == studio_hash:
                return deployment.version
        raise DeployHistoryError(f"Could not find WindowsPlayer equivalent of {version}! WindowsPlayer version with the same hash does not exist!")


    def studio_equivalent(self, version: str) -> str:
        for deployment in self.player:
            if deployment.version == version:
                player_hash = deployment.hash
                break
        else:
            raise DeployHistoryError(f"Could not find WindowsStudio64 equivalent of {version}! Given version is not WindowsPlayer")
        
        for deployment in self.studio:
            if deployment.hash == player_hash:
                return deployment.version
        raise DeployHistoryError(f"Could not find WindowsStudio64 equivalent of {version}! WindowsStudio64 version with the same hash does not exist!")


    def is_player_version(self, version: str) -> bool:
        for deployment in self.player:
            if deployment.version == version:
                return True
        return False


    def is_studio_version(self, version: str) -> bool:
        for deployment in self.studio:
            if deployment.version == version:
                return True
        return False


cache: dict = {}
def get_deploy_history(version: str) -> DeployHistory:
    if version in cache:
        return cache[version]
    
    deploy_history = DeployHistory(version)
    cache[version] = deploy_history
    return deploy_history