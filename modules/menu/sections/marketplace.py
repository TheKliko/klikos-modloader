from pathlib import Path
from typing import Optional, Literal
from tkinter import messagebox
from tempfile import TemporaryDirectory
from threading import Thread
import shutil
import os

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass, download, extract
from modules import request
from modules.request import Api, Response, ConnectionError
from modules.functions.interface.image import load as load_image, load_from_url as load_image_from_url
from modules.mod_updater import check_for_mod_updates, update_mods
from modules.launcher.deployment_info import Deployment
from modules.config import settings

from ..popup_windows.mod_download_window import ModDownloadWindow

import customtkinter as ctk


class MarketplaceSection:
    class Constants:
        SECTION_TITLE: str = "Community mods"
        SECTION_DESCRIPTION: str = "Download mods with ease"
        MOD_THUMBNAIL_SIZE: tuple[int, int] = (48, 48)
        MOD_ENTRY_INNER_PADDING: int = 4
        MOD_ENTRY_OUTER_PADDING: int = 12
        MOD_ENTRY_GAP: int = 8
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        small: ctk.CTkFont
        bold: ctk.CTkFont

    root: ctk.CTk
    container: ctk.CTkScrollableFrame
    mod_download_window: ModDownloadWindow
    data: list[dict] = []
    placeholder_image = None


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame, mod_download_window: ModDownloadWindow) -> None:
        self.root = root
        self.container = container
        self.mod_download_window = mod_download_window
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)
        self.Fonts.small = ctk.CTkFont(size=12)
        self.Fonts.bold = ctk.CTkFont(weight="bold")
        Thread(target=self._preload_data, args=(True,), daemon=True, name="marketplace-preload-thread").start()


    def _preload_data(self, ignore_errors: bool = False, ignore_thumbnails: bool = False) -> None:
        try:
            response: Response = request.get(Api.GitHub.MARKETPLACE, attempts=1, cached=True, timeout=(2, 4))
            data: list[dict] = response.json()
            self.data = data

            if ignore_thumbnails:
                return

            # if not settings.get_value("preload_marketplace_thumbnails"):
            #     return
            
            # for mod in self.data:
            #     name: str | None = mod.get("name")
            #     id: str | None = mod.get("id")
            #     if not name or not id:
            #         continue
            #     load_image_from_url(Api.GitHub.mod_thumbnail(id), size=self.Constants.MOD_THUMBNAIL_SIZE)

        except Exception:
            if not ignore_errors:
                raise


    def show(self) -> None:
        self._destroy()
        self._load_title()
        self._load_content()


    def _destroy(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()


    # region title
    def _load_title(self) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")
    # endregion


    # region content
    def _load_content(self) -> None:
        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        if not self.data:
            try:
                self._preload_data(ignore_thumbnails=True)

            except ConnectionError:
                disconnected_icon: Path = (Directory.RESOURCES / "menu" / "large" / "disconnected").with_suffix(".png")
                if not disconnected_icon.is_file():
                    restore_from_meipass(disconnected_icon)
                disconnected_image = load_image(disconnected_icon, size=(96,96))
                
                error_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
                error_frame.place(anchor="c", relx=.5, rely=.5)
                ctk.CTkLabel(error_frame, image=disconnected_image, text="").grid(column=0, row=0)
                ctk.CTkLabel(error_frame, text="Section failed to load!", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))

                return
        
        download_icon: Path = (Directory.RESOURCES / "menu" / "common" / "download").with_suffix(".png")
        if not download_icon.is_file():
            restore_from_meipass(download_icon)
        download_image = load_image(download_icon)
        
        for i, mod in enumerate(self.data):
            name: str | None = mod.get("name")
            id: str | None = mod.get("id")
            author: Optional[str] = mod.get("author")
            description: Optional[str] = mod.get("description")
            has_thumbnail: Optional[bool] = mod.get("has_thumbnail")

            if not name or not id:
                continue

            frame: ctk.CTkFrame = ctk.CTkFrame(container)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid(column=0, row=i, sticky="nsew", pady=0 if i == 0 else (self.Constants.MOD_ENTRY_GAP,0))

            # Logo
            try:
                if has_thumbnail is not True:
                    raise Exception  # Use placeholder image instead
                logo_image = load_image_from_url(Api.GitHub.mod_thumbnail(id), size=self.Constants.MOD_THUMBNAIL_SIZE)
                ctk.CTkLabel(
                    frame, image=logo_image, text="",
                    width=self.Constants.MOD_THUMBNAIL_SIZE[0], height=self.Constants.MOD_THUMBNAIL_SIZE[1]
                ).grid(column=0, row=0, padx=(self.Constants.MOD_ENTRY_OUTER_PADDING, 2*self.Constants.MOD_ENTRY_INNER_PADDING), pady=self.Constants.MOD_ENTRY_OUTER_PADDING)
            
            # Placeholder
            except Exception:
                if self.placeholder_image is None:
                    placeholder_image_path: Path = Directory.RESOURCES / "menu" / "large" / "placeholder.png"
                    if not placeholder_image_path.is_file():
                        restore_from_meipass(placeholder_image_path)
                    self.placeholder_image = load_image(placeholder_image_path, size=self.Constants.MOD_THUMBNAIL_SIZE)
                ctk.CTkLabel(
                    frame, image=self.placeholder_image, text="",
                    width=self.Constants.MOD_THUMBNAIL_SIZE[0], height=self.Constants.MOD_THUMBNAIL_SIZE[1]
                ).grid(column=0, row=0, padx=(self.Constants.MOD_ENTRY_OUTER_PADDING, 2*self.Constants.MOD_ENTRY_INNER_PADDING), pady=self.Constants.MOD_ENTRY_OUTER_PADDING)
            
            # Name, Author, Description
            name_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            name_frame.grid_columnconfigure(1, weight=1)
            name_frame.grid(column=1, row=0, sticky="new", padx=self.Constants.MOD_ENTRY_INNER_PADDING, pady=self.Constants.MOD_ENTRY_OUTER_PADDING)

            ctk.CTkLabel(name_frame, text=name, font=self.Fonts.bold, anchor="w").grid(column=0, row=0, sticky="nw")

            if author:
                ctk.CTkLabel(name_frame, text=f"({author})", font=self.Fonts.small, anchor="w").grid(column=1, row=0, sticky="nw", padx=(4,0))
            
            if description:
                ctk.CTkLabel(name_frame, text=description, anchor="w").grid(column=0, row=1, columnspan=2, sticky="nw")
            
            # Download
            ctk.CTkButton(
                frame, image=download_image, width=1, height=40, text="Download", anchor="w", compound=ctk.LEFT,
                command=lambda name=name, id=id: Thread(name=f"mod-download-thread_{id}", target=self._download_mod, args=(name, id), daemon=True).start()
            ).grid(column=2, row=0, sticky="ew", padx=(self.Constants.MOD_ENTRY_INNER_PADDING, self.Constants.MOD_ENTRY_OUTER_PADDING), pady=self.Constants.MOD_ENTRY_OUTER_PADDING)

            self.root.update_idletasks()
    # endregion


    # region functions
    # def _download_mod(self, name: str, id: str) -> None:
    #     Thread(name=f"mod-download-thread_{id}", target=self._actually_download_mod, args=(name, id), daemon=True).start()


    # The popup window freezes if I don't do it from within a thread
    def _download_mod(self, name: str, id: str) -> None:
        try:
            target_path: Path = Directory.MODS / name
            if target_path.exists():
                if not messagebox.askokcancel(ProjectData.NAME, "Another mod with the same name already exists!\nDo you wish to replace it?"):
                    return

            Logger.info(f"Downloading mod: {id}")
            textvariable: ctk.StringVar = self.mod_download_window.show(name)
            with TemporaryDirectory() as tmp:
                temporary_directory: Path = Path(tmp)
                download(Api.GitHub.mod_download(id), temporary_directory / f"{id}.zip")
                self.root.after(0, textvariable.set, "Extracting files...")
                extract(temporary_directory / f"{id}.zip", temporary_directory / id)
                self.root.after(0, textvariable.set, "Checking for updates...")

                deployment: Deployment = Deployment("Player")
                check: dict[str, list[Path]] | Literal[False] = check_for_mod_updates(temporary_directory, [id], deployment.version)
                if check:
                    self.root.after(0, textvariable.set, f"Updating {name}...")
                    update_mods(check, deployment.version, temporary_directory / "updated")

                if target_path.exists():
                    if not os.access(target_path, os.W_OK):
                        raise PermissionError(f"Write permission denied for {target_path}")
                    if target_path.is_dir():
                        shutil.rmtree(target_path)
                    elif target_path.is_file():
                        target_path.unlink()
                
                self.root.after(0, textvariable.set, "Copying files...")
                if check:
                    (temporary_directory / "updated" / id).rename(target_path)
                    # shutil.copytree(temporary_directory / "updated" / id, target_path, dirs_exist_ok=True)
                else:
                    (temporary_directory / id).rename(target_path)
                    # shutil.copytree(temporary_directory / id, target_path, dirs_exist_ok=True)

        except Exception as e:
            Logger.error(f"Failed to download mod: {id}! {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")
        
        self.mod_download_window.hide()
    # endregion