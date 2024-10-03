import sys

from modules.interface import Color


LAUNCH_MODES: dict[str,list[str]] = {
    "menu": ["-m", "--menu"],
    "launcher": ["-l", "--launch", "--launcher", "-p", "--player"],
    "studio": ["-c", "--create", "-s", "--studio"],
    "help": ["-h", "--help"]
}
DEFAULT: str = list(LAUNCH_MODES.keys())[0]

reverse_map: dict[str,str] = {}


def get() -> str:
    if not reverse_map:
        generate_reverse_map()

    args: list = sys.argv[1:]

    for item in args:
        try:
            return reverse_map[item]
        except KeyError:
            continue

    return DEFAULT


def generate_reverse_map() -> None:
    global reverse_map
    for mode, options in LAUNCH_MODES.items():
        for option in options:
            reverse_map[option] = mode


def help() -> None:
    print("Launch modes:")
    for mode, options in LAUNCH_MODES.items():
        print(Color.ACTION+mode+Color.RESET+": "+Color.TRIGGER+(Color.RESET+", "+Color.TRIGGER).join(options))
    print(Color.RESET)
    input("Press ENTER to close . . .")
    sys.exit()