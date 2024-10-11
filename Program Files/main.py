import os
import sys

python_version: str = str(sys.version_info.major)+"."+str(sys.version_info.minor)
libraries: str = os.path.join(os.path.dirname(__file__), "libraries", python_version)
os.makedirs(libraries, exist_ok=True)
sys.path.append(libraries)

from modules import exception_handler, launch_mode, startup, variables
from modules.interface import Color


root: str = os.path.dirname(os.path.dirname(__file__))


WELCOME_MESSAGE: str = r"""
,--. ,--.,--.,--.,--.          ,--.                              ,--.,--.                  ,--.               
|  .'   /|  |`--'|  |,-. ,---. |  |,---.     ,--,--,--. ,---.  ,-|  ||  | ,---.  ,--,--. ,-|  | ,---. ,--.--. 
|  .   ' |  |,--.|     /| .-. |`-'(  .-'     |        || .-. |' .-. ||  || .-. |' ,-.  |' .-. || .-. :|  .--' 
|  |\   \|  ||  ||  \  \' '-' '   .-'  `)    |  |  |  |' '-' '\ `-' ||  |' '-' '\ '-'  |\ `-' |\   --.|  |    
`--' '--'`--'`--'`--'`--'`---'    `----'     `--`--`--' `---'  `---' `--' `---'  `--`--' `---'  `----'`--'    
"""  # ASCII art generated at https://www.patorjk.com/software/taag/


def main() -> None:
    try:
        print(Color.SPLASH+WELCOME_MESSAGE+Color.RESET)

        mode: str = launch_mode.get()
        if mode == "help":
            launch_mode.help()

        variables.set("python_version", python_version)
        startup.run()
        
        import logging
        logging.debug("Launch mode: "+mode)

        if mode == "menu":
            from modules import menu
            menu.MainWindow()

        elif mode == "launcher":
            from modules import launcher
            launcher.MainWindow(mode="WindowsPlayer")

        elif mode == "studio":
            from modules import launcher
            launcher.MainWindow(mode="WindowsStudio")

    except Exception as e:
        exception_handler.run(e)


if __name__ == '__main__':
    main()