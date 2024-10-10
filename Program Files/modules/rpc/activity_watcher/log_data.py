class LogData:
    class OldLogFile:
        prefix: str = "[FLog::SingleSurfaceApp]"
        startswith: str = "unregisterMemoryPrioritizationCallback"
    class GameJoining:
        prefix: str = "[FLog::SingleSurfaceApp]"
        startswith: str = "launchUGCGameInternal"

    class GameJoin:
        prefix: str = "[FLog::GameJoinUtil]"
        startswith: str = "Game join succeeded."

    class GameTeleport:
        prefix: str = "[FLog::SingleSurfaceApp]"
        startswith: str = "initiateTeleport"

    class GamePrivateServer:
        prefix: str = "[FLog::GameJoinUtil]"
        startswith: str = "GameJoinUtil::joinGamePostPrivateServer"

    class GameReservedServer:
        prefix: str = "[FLog::GameJoinUtil]"
        startswith: str = "GameJoinUtil::initiateTeleportToReservedServer"

    class GameServerId:
        prefix: str = "[FLog::Network]"
        startswith: str = "serverId: "

    class GameData:
        prefix: str = "[FLog::Output]"
        startswith: str = "! Joining game"

    class BloxstrapRPC:
        prefix: str = "[FLog::Output]"
        startswith: str = "[BloxstrapRPC] "

    class GameLeave:
        prefix: str = "[FLog::SingleSurfaceApp]"
        startswith: str = "handleGameWillClose"


class StudioLogData:
    class OldLogFile:
        prefix: str = "[FLog::StudioApplicationState]"
        startswith: str = "AboutToQuit"

    class GameJoin:
        prefix: str = "[FLog::RobloxIDEDoc]"
        startswith: str = "RobloxIDEDoc::open - start"

    class BloxstrapRPC:
        prefix: str = "[FLog::Output]"
        startswith: str = "[BloxstrapRPC] "

    class GameLeave:
        prefix: str = "[FLog::RobloxIDEDoc]"
        startswith: str = "RobloxIDEDoc::doClose"