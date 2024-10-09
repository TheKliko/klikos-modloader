import os
import logging
import customtkinter as ctk
from typing import Literal
import time
import subprocess

from modules.filesystem import Directory
from modules.functions import latest_roblox_version, user_channel, mods, integrations
from modules.functions.wait_until_roblox_is_launched import wait_until_roblox_is_launched

from .set_launcher_stage import set_launcher_stage
from . import updater
from .close_existing_instances import close_existing_instances
from .apply_mods import apply_mods
from .apply_fastflags import apply_fastflags
from .launch_roblox import launch_roblox
from modules.functions.mod_updater import check_for_mod_updates, update_mods


def run(root: ctk.CTk, mode: Literal["WindowsPlayer","WindowsStudio"]) -> None:
    try:
        logging.info("Starting launcher tasks!")
        logging.info("Mode: "+str(mode))

        configured_mods: list = mods.get()
        active_mods: list = [mod["name"] for mod in configured_mods if (mod["enabled"] == True and os.path.isdir(os.path.join(Directory.mods(), mod["name"])))]
        do_mod_updates: bool = integrations.value("mod_updater", False)
        current_phase: int = 1
        max_phase: int = 4 if (active_mods and do_mod_updates) else 3

        set_launcher_stage(
            set_root=root,
            set_current_phase=current_phase,
            set_max_phase=max_phase,
            set_phase_name="Checking for updates . . ."
        )
        channel: str = user_channel.get(binary_type=mode)
        version: str = latest_roblox_version.get(binary_type=mode)
        logging.info("User channel: "+str(channel))
        logging.info("Roblox version: "+str(version))
        logging.info("Checking for updates . . .")
        if updater.check(binary_type=mode, channel=channel, version=version) == True:
            logging.info("Updating Roblox "+str("Player" if "player" in mode.lower() else "Studio")+" . . .")
            set_launcher_stage(
                set_phase_name="Updating Roblox . . ."
            )
            updater.run(binary_type=mode, version=version, channel=channel)
        current_phase += 1
        
        
        if active_mods and do_mod_updates:
            logging.info("Checking for mod updates . . .")
            set_launcher_stage(
                set_current_phase=current_phase,
                set_phase_name="Checking for mod updates . . ."
            )
            mod_updater_check = check_for_mod_updates(mods=active_mods, latest_version=version)
            if mod_updater_check != False:
                logging.info("Updating mods . . .")
                logging.debug("mod_updater_check = "+str(mod_updater_check))
                set_launcher_stage(
                    set_phase_name="Updating mods . . ."
                )
                update_mods(data=mod_updater_check, latest_version=version)
            current_phase += 1
        time.sleep(1)
        
        close_existing_instances(binary_type=mode)

        set_launcher_stage(
            set_current_phase=current_phase,
            set_phase_name="Applying modifications . . ."
        )
        logging.info("Applying mods . . .")
        apply_mods(mods=active_mods, version=version)
        logging.info("Applying FastFlags . . .")
        apply_fastflags(version=version)
        current_phase += 1
        time.sleep(1)
        
        set_launcher_stage(
            set_current_phase=current_phase,
            set_phase_name="Launching Roblox "+str("Player" if "player" in mode.lower() else "Studio")+" . . ."
        )
        executable: str = "RobloxPlayerBeta.exe" if "player" in mode.lower() else "RobloxStudioBeta.exe"
        logging.info("Launching Roblox . . .")
        launch_roblox(filepath=os.path.join(Directory.versions(), version, executable))
        
        wait_until_roblox_is_launched(mode="player" if "player" in mode.lower() else "studio")

        if integrations.value("discord_rpc", False) == True:
            logging.info("Starting RPC . . .")
            filepath: str = os.path.join(Directory.program_files(), "modules", "rpc", "main.py")
            command: list = ["python", filepath]
            try:
                subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                logging.warning("Failed to start RPC!")
                logging.error(type(e).__name__+": "+str(e))

        time.sleep(1)
        set_launcher_stage(destroy=True)
    
    except Exception as e:
        logging.warning("Error while running the launcher!")
        logging.error(type(e).__name__+": "+str(e))

        for widget in root.winfo_children():
            widget.destroy()
        root.destroy()
        raise