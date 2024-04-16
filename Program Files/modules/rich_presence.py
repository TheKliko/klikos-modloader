import os
import logging
import multiprocessing
import time

from packages.pypresence import Presence

from modules import variables

client_id: str = '1229494846247665775'
rpc = Presence(client_id)


def start() -> None:
    logging.info('Starting rich presence...')
    global task
    task = multiprocessing.Process(target=update, args='')
    if 'task' in globals() and task.is_alive():
        return None
    task.start()
    return None

def update() -> None:
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
    return None

def stop() -> None:
    logging.info('Stopping rich presence...')
    if 'task' in globals() and task.is_alive():
        task.terminate()
    rpc.clear()
    rpc.close()
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()