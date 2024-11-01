import os
import shutil
import threading
import queue
from tempfile import TemporaryDirectory

from modules.logger import logger
from modules.info import ProjectData
from modules.request import GitHubApi
from modules.filesystem import Directory, download, extract
from modules.functions import mod_updater
from modules.functions.get_latest_version import get_latest_version

import customtkinter as ctk


class ProgressWindow(ctk.CTkToplevel):
    stop_event: threading.Event
    def __init__(self, root: ctk.CTk, mod_id: str, mod_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.root = root
        self.mod_name = mod_name
        self.mod_id = mod_id
        self.stop_event = threading.Event()

        if self.root.icon is not None:
            self.iconbitmap(self.root.icon)
            self.after(200, lambda: self.iconbitmap(self.root.icon))
        self.title(ProjectData.NAME)

        self.protocol("WM_DELETE_WINDOW", self._set_stop_event)
        self.bind("<Escape>", lambda _: self._set_stop_event())

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.label: ctk.CTkLabel = ctk.CTkLabel(
            self,
            text=f"Downloading mod: {mod_name}"
        )
        self.label.grid(column=0, row=0, padx=32, pady=(32,0))

        progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            width=256
        )
        progress_bar.grid(column=0, row=1, padx=32, pady=(16,32))
        progress_bar.start()

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
    
    def _set_stop_event(self) -> None:
        if not self.stop_event.is_set():
            self.stop_event.set()

    def _on_close(self) -> None:
        self._set_stop_event()
        self.grab_release()
        self.destroy()

    def show(self) -> None:
        self.attributes('-topmost', True)
        self.lift()
        self.focus()
        self.grab_set()
        self.update_idletasks()
        self.wait_window()

    def close(self) -> None:
        self.after(0, self._on_close)


def marketplace_mod_download(root: ctk.CTk, mod_id: str, mod_name: str) -> None:
    logger.info(f"Downloading mod: {mod_id}...")
    exception_queue: queue.Queue = queue.Queue()

    window = ProgressWindow(root, mod_id, mod_name)
    thread: threading.Thread = threading.Thread(
        name="mod-download-thread",
        target=worker,
        args=(mod_id, mod_name, window, exception_queue),
        daemon=True
    )
    thread.start()
    window.show()

    window.close()

    if not exception_queue.empty():
        error = exception_queue.get()
        raise error


def worker(mod_id: str, mod_name: str, window: ProgressWindow, exception_queue: queue.Queue) -> None:
    try:
        target: str = os.path.join(Directory.mods(), mod_name)
        os.makedirs(Directory.mods(), exist_ok=True)

        if window.stop_event.is_set():
            return
        
        with TemporaryDirectory() as temp_directory:
            download(GitHubApi.mod_download(mod_id), os.path.join(temp_directory, f"{mod_name}.zip"))
            if window.stop_event.is_set():
                return
            
            extract(os.path.join(temp_directory, f"{mod_name}.zip"), os.path.join(temp_directory, mod_name))
            if window.stop_event.is_set():
                return

            if os.path.isdir(target):
                shutil.rmtree(target, ignore_errors=True)
            shutil.copytree(os.path.join(temp_directory, mod_name), target, dirs_exist_ok=True)
            if window.stop_event.is_set():
                return
            
            if not os.path.isfile(os.path.join(temp_directory, mod_name, "info.json")):
                return

            latest_version: str = get_latest_version("WindowsPlayer")
            check = mod_updater.check_for_mod_updates([os.path.join(temp_directory, mod_name)], latest_version)
            if window.stop_event.is_set():
                return
            elif check:
                window.label.configure(text=f"Updating mod: {mod_name}")
                mod_updater.update_mods(check, latest_version, os.path.join(temp_directory, "_updated"))
                if window.stop_event.is_set():
                    return
                
                if not os.path.isdir(os.path.join(temp_directory, "_updated", mod_name)):
                    return
                shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(os.path.join(temp_directory, "_updated", mod_name), target, dirs_exist_ok=True)
    
    except Exception as e:
        exception_queue.put(e)

    finally:
        window.close()