import os
import sys

ROOT: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'libraries'))

from modules import exception_handler
from modules import interface
from modules.process import startup
from modules.process.get_launch_mode import get_launch_mode
from modules.process import menu
from modules.process import launcher
from modules.process import shutdown
from modules.utils import variables
from modules.other.launch_mode import MODLOADER_MENU, ROBLOX_PLAYER, ROBLOX_STUDIO


WELCOME_MESSAGE: str = r"""
,--. ,--.,--.,--.,--.          ,--.                              ,--.,--.                  ,--.               
|  .'   /|  |`--'|  |,-. ,---. |  |,---.     ,--,--,--. ,---.  ,-|  ||  | ,---.  ,--,--. ,-|  | ,---. ,--.--. 
|  .   ' |  |,--.|     /| .-. |`-'(  .-'     |        || .-. |' .-. ||  || .-. |' ,-.  |' .-. || .-. :|  .--' 
|  |\   \|  ||  ||  \  \' '-' '   .-'  `)    |  |  |  |' '-' '\ `-' ||  |' '-' '\ '-'  |\ `-' |\   --.|  |    
`--' '--'`--'`--'`--'`--'`---'    `----'     `--`--`--' `---'  `---' `--' `---'  `--`--' `---'  `----'`--'    
"""  # ASCII art generated at https://www.patorjk.com/software/taag/


def main() -> None:
    try:
        variables.set('root', ROOT)

        interface.clear()
        interface.Print(WELCOME_MESSAGE, color=interface.Color.SPLASH)

        startup.run()

        mode: list[str] = get_launch_mode()
        if mode == MODLOADER_MENU:
            menu.run()
        else:
            launcher.run(mode)

    
    except shutdown.ManualQuitOut as e:
        pass


    except Exception as e:
        exception_handler.run(e)


    finally:
        shutdown.run()


if __name__ == '__main__':
    main()