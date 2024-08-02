import os


class RichPresenceStatus():
    MENU: str = 'MENU'
    LAUNCHER: str = 'LAUNCHER'
    ERROR: str = 'ERROR'
    PLAYING: str = 'PLAYING'
    CREATING: str = 'CREATING'
    ROBLOX: str = 'ROBLOX'
    STUDIO: str = 'STUDIO'


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()