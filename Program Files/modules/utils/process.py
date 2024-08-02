import logging
import os
import subprocess


def close(process_name: str) -> None:
    """
    Close a given process
    
    :param process_name: The process to close
    
    :type process_name: str
    
    :rtype None
    :return None
    """

    logging.info(f'Closing process: {process_name}')
    COMMAND: str = f'taskkill /f /im {process_name}'
    subprocess.run(COMMAND, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def exists(process_name: str) -> bool:  # Check if process exists using https://stackoverflow.com/a/29275361
    """
    Check if a given process exists
    
    :param process_name: The process to check
    
    :type process_name: str
    
    :rtype bool
    :return True of the process exists, otherwise False
    """

    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()