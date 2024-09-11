import os

from .exceptions import FileSystemError


def verify(path: str, create_missing_directories: bool = False, create_missing_file: bool = False) -> None:
    if not os.path.exists(path):
        if create_missing_directories == False and create_missing_file == False:
            raise FileSystemError(f'Path does not exist: {path}')
        
        os.makedirs(path, exist_ok=True)
        
        if create_missing_file == True:
            with open(path, 'w') as file:
                file.close()