class LogData:
    class OldLogFile:
        prefix: str = "[FLog::SingleSurfaceApp]"
        startswith: str = "unregisterMemoryPrioritizationCallback"
    
    class GameCrash:
        startswith: str = "RBXCRASH"

    class GameJoin:
        prefix: str = "[FLog::Output]"
        startswith: str = "! Joining game "

    # class GameTeleport:
    #     prefix: str = "[FLog::SingleSurfaceApp]"
    #     startswith: str = "initiateTeleport"

    # class GamePrivateServer:
    #     prefix: str = "[FLog::GameJoinUtil]"
    #     startswith: str = "GameJoinUtil::joinGamePostPrivateServer"

    # class GameReservedServer:
    #     prefix: str = "[FLog::GameJoinUtil]"
    #     startswith: str = "GameJoinUtil::initiateTeleportToReservedServer"

    class BloxstrapRPC:
        prefix: str = "[FLog::Output]"
        startswith: str = "[BloxstrapRPC] "

    class GameLeave:
        prefix: str = "[FLog::SingleSurfaceApp]"
        startswith: str = "handleGameWillClose"


class StudioLogData:
    class OldLogFile:
        prefix: str = "[FLog::Output]"
        startswith: str = "About to exit the application, doing cleanup."

    class GameJoin:
        prefix: str = "[FLog::StudioKeyEvents]"
        startswith: str = "open place (identifier = "
        endswith: str = ") [start]"

    class BloxstrapRPC:
        prefix: str = "[FLog::Output]"
        startswith: str = "[BloxstrapRPC] "

    class GameLeave:
        prefix: str = "[FLog::Output]"
        startswith: str = "close IDE doc"