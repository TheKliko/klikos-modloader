import os
import shutil


class ValidationError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


class FileSystemError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


class ValidationMode:  # POV: You just learned about classes and now you need an excuse to use it everywhere you can
    FILE: str = 'FILE'
    DIRECTORY: str = 'DIRECTORY'
    MIXED: str = 'MIXED'


# Made this a lot more complicated than it had to be, but it's too late now to change it
def validate(items: str | list[str] | dict[str, str | list[str]], mode: str = ValidationMode.FILE, create_missing_directories: bool = True, silent: bool = False) -> None:
    """
    Check if a file or directory exists, with options to create missing directories and suppress error messages
    
    :param items: The files or directories to validate
    :param mode: (optional) Specify whether to check for files or directories. Default: ValidationMode.FILE
    :param create_missing_directories: (optional) Create directories if they do not exist. Default: True
    :param silent: (optional) Suppress error messages. Default: False
    
    :type data: str | list[str] | dict[str, str | list[str]]
    :type mode: str
    :type create_missing_directories: bool
    :type silent: bool
    
    :rtype None
    :return None
    """

    def check_file(file: str):
        """Check whether the given path is a file, otherwise raises a ValidationError"""
        if not os.path.isfile(file) and not silent:
            raise ValidationError(f'File does not exist: {os.path.basename(file)}')

    def check_directory(directory: str):
        """Check whether the given path is a directory, otherwise raises a ValidationError"""
        if not os.path.isdir(directory):
            if create_missing_directories:
                os.makedirs(directory)

            elif not silent:
                raise ValidationError(f'Directory does not exist: {os.path.basename(directory)}')


    MODE: str = mode.upper()  


    # Single file or directory
    if isinstance(items, str) and MODE == ValidationMode.FILE:
        check_file(items)

    elif isinstance(items, str) and MODE == ValidationMode.DIRECTORY:
        check_directory(items)
    

    # Multiple files or directories
    elif isinstance(items, list) and MODE == ValidationMode.FILE:
        for file in items:
            check_file(file)
            
    elif isinstance(items, list) and MODE == ValidationMode.DIRECTORY:
        for directory in items:
            check_file(directory)
    

    # Files & directories
    elif isinstance(items, dict) or isinstance(items, dict) and MODE == ValidationMode.MIXED:
        if not 'files' in items.keys() or not 'directories' in items.keys():
            raise ValidationError('Invalid request: files/directories are not defined')
        
        files: str | list[str] = items['files']
        directories: str | list[str] = items['directories']
        
        if isinstance(files, str):
            check_file(files)

        elif isinstance(directories, str):
            check_file(directories)
        
        elif isinstance(files, list):
            for file in files:
                check_file(file)
        
        elif isinstance(directories, list):
            for directory in directories:
                check_directory(directory)
        
        else:
            raise ValidationError('Invalid request: Invalid instance')
    
    else:
        raise ValidationError('Invalid request: Invalid validation mode')


def subdirectories(path: str, complete_filepath: bool = False) -> list[str]:
    """
    Get a list of direct child directories in a given directory
    
    :param path: The path to the parent directory
    :param complete_filepath: (optional) List the complete path, instead of only the name of each subdirectory. Default: False
    
    :type path: str
    :type complete_filepath: bool
    
    :rtype list[str]
    :return The subdirectories in a given directory
    """

    validate(path, ValidationMode.DIRECTORY)
    
    subdirectories: list[str] = os.listdir(path)

    if complete_filepath == True:
        return [os.path.join(path, folder) for folder in subdirectories]
    
    return subdirectories


def copy_directory(source: str, destination: str):
    """
    Copy all files within a given directory to a different directory
    
    :param source: The path to the source directory
    :param destination: The path to the target directory
    
    :type source: str
    :type destination: str
    
    :rtype list[str]
    :return The subdirectories in a given directory
    """

    validate(source, ValidationMode.DIRECTORY, create_missing_directories=False)
    try:
        shutil.copytree(source, destination, dirs_exist_ok=True)
    except Exception as e:
        raise FileSystemError(f'[{type(e).__name__}] {str(e)}')


def remove_directory(items: str | list) -> None:
    """
    Remove the given directory
    
    :param items: The directory to remove
    
    :type items: str
    
    :rtype None
    :return None
    """

    if isinstance(items, str):
        try:
            shutil.rmtree(items, True)
        except Exception as e:
            raise FileSystemError(f'[{type(e).__name__}] {str(e)}')
    
    elif isinstance(items, list):
        for item in items:
            try:
                shutil.rmtree(item, True)
            except Exception as e:
                raise FileSystemError(f'[{type(e).__name__}] {str(e)}')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()