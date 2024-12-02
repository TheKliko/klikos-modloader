import sys


MODES: dict[str,list[str]] = {
    "menu": ["-m", "--menu"],
    "player": ["-l", "--launch", "--launcher", "-p", "--player"],
    "studio": ["-c", "--create", "-s", "--studio"],
    "rpc": ["-rpc", "--presence"]
}
DEFAULT: str = list(MODES.keys())[0]
REVERSE_MAP: dict[str,str] = {option: mode for mode, options in MODES.items() for option in options}


def get() -> str:
    args: list = sys.argv[1:]

    for item in args:
        mode = REVERSE_MAP.get(item)
        if mode is not None:
            return mode

    return DEFAULT