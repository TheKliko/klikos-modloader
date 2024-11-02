import sys


LAUNCH_MODES: dict[str,list[str]] = {
    "menu": ["-m", "--menu"],
    "bloxstrap": ["--bloxstrap"]
}
DEFAULT: str = list(LAUNCH_MODES.keys())[0]

reverse_map: dict[str,str] = {}


def get() -> str:
    generate_reverse_map()

    args: list = sys.argv[1:]

    for item in args:
        mode = reverse_map.get(item)
        if mode is not None:
            return mode

    return DEFAULT


def generate_reverse_map() -> None:
    for mode, options in LAUNCH_MODES.items():
        for option in options:
            reverse_map[option] = mode