class LogData:
    class Player:
        class OldlogFile:
            prefix: str = "[FLog::SingleSurfaceApp]"
            keyword: str = "unregisterMemoryPrioritizationCallback"

        class GameLeave:
            prefix: str = "[FLog::SingleSurfaceApp]"
            keyword: str = "leaveUGCGameInternal"

        class GameJoin:
            prefix: str = "[FLog::Output]"
            keyword: str = "! Joining game "

        class GameJoinLoadTime:
            prefix: str = "[FLog::GameJoinLoadTime]"
            keyword: str = "Report game_join_loadtime"

        class GamePrivateServer:
            prefix: str = "[FLog::GameJoinUtil]"
            keyword: str = "GameJoinUtil::joinGamePostPrivateServer"

        class GameReservedServer:
            prefix: str = "[FLog::GameJoinUtil]"
            keyword: str = "GameJoinUtil::initiateTeleportToReservedServer"

        class BloxstrapRPC:
            prefix: str = "[FLog::Output]"
            bloxstrap_rpc_prefix: str = "[BloxstrapRPC]"


    class Studio:
        class OldLogFile:
            prefix: str = "[FLog::Output]"
            keyword: str = "About to exit the application, doing cleanup."
            
        class GameLeave:
            prefix: str = "[FLog::StudioKeyEvents]"
            keyword: str = "close IDE doc"

        class GameJoin:
            prefix: str = "[FLog::StudioKeyEvents]"
            keyword: str = "open place"