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


def have_same_git_hash(version_1: str, version_2: str) -> bool:
    if version_1 == version_2:
        return True

    history: list = deploy_history.get().ALL

    git_hash_1 = None
    git_hash_2 = None

    for item in history:
        version = item["version"]
        git_hash = item["git_hash"]

        if version == version_1 and git_hash_1 is None:
            git_hash_1 = git_hash
        
        elif version == version_2 and git_hash_2 is None:
            git_hash_2 is git_hash
        
        if git_hash_1 is not None and git_hash_2 is not None:
            return git_hash_1 == git_hash_2
    
    return True


def get_git_hash(version: str) -> str|None:
    history:  list = deploy_history.get().ALL

    for item in history:
        if item["version"] == version:
            return item["git_hash"]
    
    return None


def get_studio_version(git_hash: str) -> str|None:
    history:  list = deploy_history.get().ROBLOX_STUDIO

    for item in history:
        if item["git_hash"] == git_hash:
            return item["version"]
    
    return None