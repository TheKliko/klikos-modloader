import os
import sys

python_version: str = str(sys.version_info.major)+"."+str(sys.version_info.minor)
libraries: str = os.path.join(os.path.dirname(__file__), "libraries", python_version)
os.makedirs(libraries, exist_ok=True)
sys.path.append(libraries)

import exception_handler
from modules import launch_mode
from modules import startup
from modules import variables
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

        if mode == "menu":
            pass
        elif mode == "launcher":
            pass
        elif mode == "studio":
            pass

    except Exception as e:
        exception_handler.run(e)


if __name__ == '__main__':
    main()