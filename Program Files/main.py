import os
import sys

python_version: str = f'{sys.version_info.major}.{sys.version_info.minor}'
ROOT: str = os.path.dirname(os.path.dirname(__file__))

path_to_libraries: str = os.path.join(os.path.dirname(__file__), 'libraries')
path_version_specific_libraries: str = os.path.join(os.path.dirname(__file__), 'version_specific_libraries', f'python-{python_version}')

try:
    os.makedirs(path_to_libraries, exist_ok=True)
    os.makedirs(path_version_specific_libraries)
except:
    pass

sys.path.append(path_to_libraries)
sys.path.append(path_version_specific_libraries)

from modules import exception_handler
from modules import interface
from modules.process import startup
from modules.process.get_launch_mode import get_launch_mode
from modules.process import shutdown
from modules.utils import variables
from modules.other.launch_mode import MODLOADER_MENU


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
        variables.set('python_version', python_version)

        interface.clear()
        interface.Print(WELCOME_MESSAGE, color=interface.Color.SPLASH)
        
        startup.run()

        from modules.process import menu
        from modules.process import launcher

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