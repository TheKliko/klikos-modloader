import ctypes

from modules import Logger


def create_singleton_mutex() -> None:
    kernel32 = ctypes.windll.kernel32
    mutexes: list[str] = ["ROBLOX_singletonMutex", "ROBLOX_singletonEvent"]

    for mutex_name in mutexes:
        Logger.info(f"Creating mutex: {mutex_name}", prefix="launcher.tasks.create_singleton_mutex()")
        mutex = kernel32.CreateMutexW(None, False, mutex_name)

        if mutex == 0:
            Logger.warning(f"Failed to create mutex: {mutex_name}. {ctypes.WinError()}", prefix="launcher.tasks.create_singleton_mutex()")
            return
        
        if kernel32.GetLastError() == 193:
            Logger.warning(f"Mutex already exists: {mutex_name}", prefix="launcher.tasks.create_singleton_mutex()")
        else:
            Logger.info("Mutex created successfully!", prefix="launcher.tasks.create_singleton_mutex()")
