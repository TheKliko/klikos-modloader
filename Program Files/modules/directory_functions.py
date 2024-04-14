import os
import logging
import shutil


def copy_directory(source: str, destination: str) -> None:
    try:
        shutil.copytree(src=source, dst=destination, dirs_exist_ok=True)
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def create_directory(path: str, name: str | None = None) -> None:
    if name:
        logging.warn(f'Creating directory: {os.path.basename(name)}')
        try:
            os.makedirs(name=os.path.join(path, name), exist_ok=True)
        
        except Exception as e:
            logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    else:
        logging.warn(f'Creating directory: {os.path.basename(path)}')
        try:
            os.makedirs(path, exist_ok=True)
        
        except Exception as e:
            logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def remove_directory(source: str, name: str | None = None) -> None:
    if not name:
        logging.warn(f'Removing directory: {os.path.basename(source)}')
    else:
        logging.warn(f'Removing directory: {name}')
    try:
        shutil.rmtree(source)

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()