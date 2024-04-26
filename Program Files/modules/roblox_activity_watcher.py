import os
import time
import logging
import glob
import re

from modules import variables

logs_directory: str = os.path.join(str(os.getenv('LOCALAPPDATA')), 'Roblox/Logs')


def update_roblox_activity_status() -> list | None:
    activity_status =  read_logs()
    if not activity_status:
        variables.set(name='rich_presence_game_id', value='not_in_game')
        variables.set(name='in_game', value=False)
    
    elif 'gamejoin' in activity_status:
        game_id = activity_status[1]
        variables.set(name='rich_presence_game_id', value=game_id)
        if not variables.get(name='in_game'):
            variables.set(name='in_game', value=True)
            variables.set(name='in_game_timestamp', value=int(time.time()))

    elif 'gameleave' in activity_status:
        variables.set(name='rich_presence_game_id', value='not_in_game')
        variables.set(name='in_game', value=False)

    return None

def read_logs() -> list:
    try:
        list_of_files = glob.glob(f'{logs_directory}/*')
        latest_file = max(list_of_files, key=os.path.getmtime)
        with open(latest_file, 'r') as log:
            data = log.read()
            log.close()


        if '[FLog::SingleSurfaceApp] unregisterMemoryPrioritizationCallback' in data:
            return ['gameleave']
        # old_log = None
        # old_log = [line for line in data.split('\n') if '[FLog::SingleSurfaceApp] unregisterMemoryPrioritizationCallback' in line]

        # if old_log:
        #     return ['gameleave']
        
        gamejoins = [line for line in data.split('\n') if '[FLog::GameJoinLoadTime]' in line]
        gameleaves = [line for line in data.split('\n') if '[FLog::SingleSurfaceApp] handleGameWillClose' in line]
        if len(gamejoins) == len(gameleaves):
            return ['gameleave']
        
        pattern = pattern = r'placeid:(\d+)'
        match = re.search(pattern, gamejoins[-1])
        if not match:
            return ['gameleave']
        
        game_id = match.group(1)
        value = ['gamejoin', game_id]
        return value


    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    read_roblox_logs()
    input('debug')
    main()