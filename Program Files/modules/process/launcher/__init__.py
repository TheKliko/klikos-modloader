import logging
import subprocess
import time

from modules import interface
from modules.other.launch_mode import ROBLOX_STUDIO
from modules.roblox import channel, update, launcher
from modules.utils import variables
from modules import activity_watcher

from . import mods
from . import fastflags


def run(mode: list[str]) -> None:
    binary_type: str = 'WindowsStudio' if mode == ROBLOX_STUDIO else 'WindowsPlayer'
    logging.info(f'Sarting launcher in "{binary_type}" mode . . .')
    variables.set('binary_type', binary_type)


    # Close existing Roblox instances
    subprocess.Popen(
        f'taskkill /f /im Roblox{binary_type.removeprefix('Windows')}Beta.exe',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


    terminal = interface.Interface(section='Launcher')
    terminal.add_line('Checking for Roblox updates . . .')
    terminal.add_divider()
    
    user_channel: str = channel.get(binary_type)
    update_available, version = update.check(binary_type, user_channel)
    if update_available == True:
        terminal.remove_last(2)
        terminal.add_line('Updating Roblox . . .')
        terminal.add_divider()
        update.install(binary_type, user_channel, version)

    else:
        terminal.remove_last(2)
        terminal.add_line('No Roblox updates found!')
        terminal.add_divider()

    
    active_mods: list[str] = mods.get_active()
    mods.update({}, version)

    if active_mods != []:
        auto_update_mods = variables.get('auto_update_mods', {}).get('value', False)
        if auto_update_mods:
            outdated_mods: dict[str, list[str]] = mods.get_outdated_mods(version, active_mods)
            if outdated_mods != {}:
                terminal.remove_last(1)
                terminal.add_line('Updating mods . . . (This may take a few minutes)')
                terminal.add_divider()
                mods.update(outdated_mods, version)
                terminal.remove_last(1)

        terminal.remove_last(1)
        terminal.add_line('Applying mods . . .')
        terminal.add_divider()
        mods.apply(active_mods, version)


    terminal.remove_last(1)
    terminal.add_line('Applying FastFlags . . .')
    terminal.add_divider()
    fastflags.apply(version)


    terminal.remove_last()
    terminal.add_line('Launching Roblox . . .')
    terminal.add_divider()
    launcher.launch(binary_type, version)


    discord_rpc: bool = variables.get('discord_rpc', {}).get('value', False)
    server_notification: bool = variables.get('server_notification', {}).get('value', False)

    if discord_rpc == False and server_notification == False:
        logging.info('Activity watcher: off')
        terminal.add_line('Roblox should launch shortly, this program will now terminate', alignment=interface.Alignment.CENTER)
        terminal.add_divider()
        time.sleep(2)
        return

    logging.info('Activity watcher: on')
    terminal.add_line('Roblox should launch shortly, this program will now minimize', alignment=interface.Alignment.CENTER)
    terminal.add_divider()
    
    if discord_rpc == True and server_notification == True:
        terminal.add_line('It will keep running in the background in order to update your Discord RPC status and send server notifications')
    elif discord_rpc == True and server_notification == False:
        terminal.add_line('It will keep running in the background in order to update your Discord RPC status')
    elif discord_rpc == False and server_notification == True:
        terminal.add_line('It will keep running in the background in order to send server notifications')
    terminal.add_line('This can be turned off in settings')
    terminal.add_divider()
    time.sleep(2)
    interface.hide()

    activity_watcher.start(binary_type)