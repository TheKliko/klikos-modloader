from . import deploy_history


def get_studio_equivalent(guid: str) -> str|None:
    history: deploy_history.DeployHistory = deploy_history.get()
    player_history: list = history.ROBLOX_PLAYER
    studio_history: list = history.ROBLOX_STUDIO

    for item in player_history:
        if item["version"] == guid:
            git_hash: str = item["git_hash"]
            break
    else:
        return None
    
    for item in studio_history:
        if item["git_hash"] == git_hash:
            version: str = item["version"]
            break
    else:
        return None

    return version


def get_player_equivalent(guid: str) -> str|None:
    history: deploy_history.DeployHistory = deploy_history.get()
    player_history: list = history.ROBLOX_PLAYER
    studio_history: list = history.ROBLOX_STUDIO

    for item in studio_history:
        if item["version"] == guid:
            git_hash: str = item["git_hash"]
            break
    else:
        return None

    for item in player_history:
        if item["git_hash"] == git_hash:
            version: str = item["version"]
            break
    else:
        return None

    return version