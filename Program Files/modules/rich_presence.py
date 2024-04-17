import os
import subprocess
import logging
import multiprocessing
import time

from packages.pypresence import Presence
from packages.pypresence import exceptions as pypresence_exceptions

from modules import variables

client_id: str = '1229494846247665775'
rpc = Presence(client_id)

def start() -> None:
    logging.info('Starting rich presence...')
    if not process_exists('RobloxPlayerBeta.exe'):
        logging.warning('Failed to start rich presence: Discord not found')
        return None
    global task
    task = multiprocessing.Process(target=update, args='')
    if 'task' in globals() and task.is_alive():
        return None
    task.start()
    return None

def update() -> None:
    try:
        rpc.connect()
        while True:
            details = variables.get(name='rich_presence_details')
            timestamp = variables.get(name='rich_presence_timestamp')
            if not details or not timestamp:
                stop()
                return None
            rpc.update(
                details=details,
                start=timestamp,
                large_image='logo',
                large_text='Kliko\'s modloader'
            )
            time.sleep(5)

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    
    return None

def stop() -> None:
    logging.info('Stopping rich presence...')
    if 'task' in globals() and task.is_alive():
        task.terminate()
    rpc.clear()
    rpc.close()
    return None

# Check if process exists using https://stackoverflow.com/a/29275361
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()