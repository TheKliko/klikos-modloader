import sys

from modules import Logger  # Imported first to initialize the logger
from modules import LaunchMode, exception_handler, startup


def main() -> None:
    if getattr(sys, "frozen", False):
        import pyi_splash
        if pyi_splash.is_alive():
            pyi_splash.close()

    try:
        startup.run()
        
        match LaunchMode.get().lower():
            case "menu":
                input("Menu")
            case "player":
                input("Player")
            case "studio":
                input("Studio")
            case "rpc":
                input("RPC")

    except Exception as e:
        exception_handler.run(e)
    
    finally:
        Logger.info("Shutting down...")


if __name__ == "__main__":
    main()