"""# directory.py

directory.py is a module used in Kliko's modloader,
it's purpose is to take care of functions related to directories.
"""


import os


def subdirectories(path: str) -> list[str]:
    """Returns a list containing all subdirectories in a given directory

    :param path: The path to a directory
    :type path: str
    :rtype list[str] | None
    :return A list containing the names of the subdirectories in a given directory if they exist, otherwise an empty list
    """

    subdirectories = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            subdirectories.append(item)

    return subdirectories


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()