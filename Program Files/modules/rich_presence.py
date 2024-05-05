import os
import subprocess
import logging
import multiprocessing
import time

from packages.pypresence import Presence
from packages.pypresence import exceptions as pypresence_exceptions

from modules import variables
from modules.roblox_activity_watcher import update_roblox_activity_status
from modules.request_handler import request_json

client_id: str = '1229494846247665775'
rpc = Presence(client_id)

def start() -> None:
    logging.info('Starting rich presence...')
    if not process_exists('Discord.exe'):
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
            update_roblox_activity_status()
            details = variables.get(name='rich_presence_details')
            timestamp = variables.get(name='rich_presence_timestamp')
            large_image = variables.get(name='rich_presence_large_image')
            large_text = 'Kliko\'s modloader'
            small_image = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/launcher-small.png'
            game_id = variables.get(name='rich_presence_game_id')
            if not game_id == 'not_in_game':
                config = request_json(source=r'https://www.roblox.com/item-thumbnails?params=%5B%7BassetId:' + game_id + r'%7D%5D')
                large_image = config[0]['thumbnailUrl']
                large_text = config[0]['name']
                details = f'Playing {config[0]['name']}'
            buttons = [{"label": "Learn more", "url": "https://thekliko.github.io/klikos-modloader"}]
            if not large_image:
                large_image='logo'

            if variables.get(name='in_game'):
                timestamp = variables.get(name='in_game_timestamp')
            elif not variables.get(name='in_menu'):
                small_image = 'none'

            rpc.update(
                details=details,
                start=timestamp,
                large_image=large_image,
                large_text=large_text,
                buttons=buttons,
                small_image=small_image,
                small_text='Kliko\'s modloader'
            )

            time.sleep(5)
    
    # Reconnect rpc after switching accounts. Gives EOFError if asking for input later, also breaks logging for some reason
    except (pypresence_exceptions.PipeClosed, pypresence_exceptions.DiscordError) as e:
        initialize_logger()
        logging.warning(f'pypresence {type(e).__name__} occurred: {e}')
        start()

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

def initialize_logger() -> None:
    logging_filename: str = variables.get(name='logging_filename')
    from main import logging_directory
    logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(funcName)s] [line_%(lineno)d]: %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S',
    filename=os.path.join(logging_directory, logging_filename),
    encoding='utf-8',
    level=logging.DEBUG
    )



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()