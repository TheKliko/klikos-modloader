import os

from modules.presence import rpc


def run() -> None:
    """Begin the shutdown process"""

    rpc.stop()


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()