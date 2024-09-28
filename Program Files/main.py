import os
import sys

python_version: str = str(sys.version_info.major)+"."+str(sys.version_info.minor)

path_to_common_libraries: str = os.path.join(os.path.dirname(__file__), "libraries", "common")
path_to_version_specific_libraries: str = os.path.join(os.path.dirname(__file__), "libraries", python_version)

os.makedirs(path_to_common_libraries, exist_ok=True)
os.makedirs(path_to_version_specific_libraries, exist_ok=True)

sys.path.append(path_to_common_libraries)
sys.path.append(path_to_version_specific_libraries)

import exception_handler
from modules import startup
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
        # startup.logger()
        exit(9009)
        startup.run()
        raise OSError("testing")


    except Exception as e:
        exception_handler.run(e)


if __name__ == '__main__':
    main()