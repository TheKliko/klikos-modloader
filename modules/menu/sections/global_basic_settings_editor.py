from pathlib import Path
from xml.etree import ElementTree as xml
from typing import Any
from tkinter.messagebox import showwarning

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import File, Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class GlobalBasicSettingsSection:
    class Constants:
        SECTION_TITLE: str = "GlobalBasicSettings Editor"
        SECTION_DESCRIPTION: str = "Don't change these settings unless you know what you're doing"
        ENTRY_INNER_PADDING: int = 4
        ENTRY_OUTER_PADDING: int = 12
        ENTRY_GAP: int = 8
        ALLOWED_TAGS: list[str] = ["bool", "token", "string", "int", "float", "Vector2"]


    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        bold: ctk.CTkFont


    root: ctk.CTk
    container: ctk.CTkScrollableFrame


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame) -> None:
        self.root = root
        self.container = container
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)
        self.Fonts.bold = ctk.CTkFont(weight="bold")


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
        container.grid_columnconfigure((0, 1), weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        if not File.GLOBAL_BASIC_SETTINGS.is_file():
            not_found_icon: Path = (Directory.RESOURCES / "menu" / "large" / "file-not-found").with_suffix(".png")
            if not not_found_icon.is_file():
                restore_from_meipass(not_found_icon)
            not_found_image = load_image(not_found_icon, size=(96,96))
            
            error_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
            error_frame.place(anchor="c", relx=.5, rely=.5)
            ctk.CTkLabel(error_frame, image=not_found_image, text="").grid(column=0, row=0)
            ctk.CTkLabel(error_frame, text=f"File not found: {File.GLOBAL_BASIC_SETTINGS.name}", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))
            
            return
        
        tree: xml.ElementTree = xml.parse(File.GLOBAL_BASIC_SETTINGS)
        root = tree.getroot()
        properties = root.find(".//Properties")

        if properties is None:
            not_found_icon: Path = (Directory.RESOURCES / "menu" / "large" / "file-not-found").with_suffix(".png")
            if not not_found_icon.is_file():
                restore_from_meipass(not_found_icon)
            not_found_image = load_image(not_found_icon, size=(96,96))
            
            error_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
            error_frame.place(anchor="c", relx=.5, rely=.5)
            ctk.CTkLabel(error_frame, image=not_found_image, text="").grid(column=0, row=0)
            ctk.CTkLabel(error_frame, text=f"Failed to read {File.GLOBAL_BASIC_SETTINGS.name}", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))
            
            return
        
        i: int = 0
        for element in properties:
            if element.tag not in self.Constants.ALLOWED_TAGS:
                continue

            if "name" not in element.attrib:
                continue
            
            frame: ctk.CTkFrame = ctk.CTkFrame(container, width=(container.winfo_width()//2)-self.Constants.ENTRY_GAP)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_propagate(True)
            frame.grid(column=self._get_frame_column(i), row=self._get_frame_row(i), sticky="nsew", pady=self._get_frame_pady(i), padx=self._get_frame_padx(i))
            i += 1

            # Name label
            ctk.CTkLabel(frame, text=f"[{element.tag.upper()}] {element.attrib['name']}", anchor="w", font=self.Fonts.bold).grid(column=0, row=0, sticky="nw", padx=self.Constants.ENTRY_OUTER_PADDING, pady=(self.Constants.ENTRY_OUTER_PADDING, self.Constants.ENTRY_INNER_PADDING))

            # Content
            content_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            content_frame.grid(column=0, row=1, sticky="nsew", padx=self.Constants.ENTRY_OUTER_PADDING, pady=(0, self.Constants.ENTRY_OUTER_PADDING))

            match element.tag:
                # region Vector2
                case "Vector2":
                    x_value = element.find("X")
                    if x_value is None:
                        x_value = "N/A"
                    else:
                        x_value = "N/A" if x_value.text is None else x_value.text.strip()
                        
                    y_value = element.find("Y")
                    if y_value is None:
                        y_value = "N/A"
                    else:
                        y_value = "N/A" if y_value.text is None else y_value.text.strip()

                    ctk.CTkLabel(content_frame, text="X: ", anchor="e").grid(column=0, row=0, sticky="nsew")
                    x_entry = ctk.CTkEntry(
                        content_frame, width=40, height=40, validate="key",
                        validatecommand=(self.root.register(lambda value: value.isdigit() or value == ""), '%P')
                    )
                    x_entry.insert("end", x_value)
                    x_entry.bind("<Return>", lambda _: self.root.focus())
                    x_entry.bind("<Control-s>", lambda _: self.root.focus())
                    x_entry.bind("<FocusOut>", lambda event, name=element.attrib['name']: self._update_vector2_x_value(tree=tree, name=name, event=event))
                    x_entry.grid(column=1, row=0, sticky="ew", padx=(0, self.Constants.ENTRY_INNER_PADDING))

                    ctk.CTkLabel(content_frame, text="Y: ", anchor="e").grid(column=2, row=0, sticky="nsew")
                    y_entry = ctk.CTkEntry(
                        content_frame, width=40, height=40, validate="key",
                        validatecommand=(self.root.register(lambda value: value.isdigit() or value == ""), '%P')
                    )
                    y_entry.insert("end", y_value)
                    y_entry.bind("<Return>", lambda _: self.root.focus())
                    y_entry.bind("<Control-s>", lambda _: self.root.focus())
                    y_entry.bind("<FocusOut>", lambda event, name=element.attrib['name']: self._update_vector2_y_value(tree=tree, name=name, event=event))
                    y_entry.grid(column=3, row=0, sticky="ew")

                # region bool
                case "bool":
                    value = element.text or "false"
                    value = value.strip()
                    value = value == "true"

                    ctk.CTkLabel(content_frame, text="Value: ", anchor="e").grid(column=0, row=0, sticky="nsew")
                    var: ctk.BooleanVar = ctk.BooleanVar(value=value)
                    ctk.CTkSwitch(
                        content_frame, text="", width=48, variable=var, onvalue=True, offvalue=False,
                        command=lambda var=var, name=element.attrib['name']: self._update_bool_value(tree=tree, name=name, value=var.get())
                    ).grid(column=1, row=0, sticky="e", padx=(8, 0))
                
                # region int
                case "int":
                    content_frame.grid_columnconfigure(1, weight=1)

                    value = element.text or ""
                    value = value.strip()

                    ctk.CTkLabel(content_frame, text="Value: ", anchor="e").grid(column=0, row=0, sticky="nsew")
                    entry = ctk.CTkEntry(
                        content_frame, width=40, height=40, validate="key",
                        validatecommand=(self.root.register(lambda value: value.isdigit() or value == ""), '%P')
                    )
                    entry.insert("end", value)
                    entry.bind("<Return>", lambda _: self.root.focus())
                    entry.bind("<Control-s>", lambda _: self.root.focus())
                    entry.bind("<FocusOut>", lambda event, name=element.attrib['name']: self._update_int_value(tree=tree, name=name, event=event))
                    entry.grid(column=1, row=0, sticky="ew", padx=(0, self.Constants.ENTRY_INNER_PADDING))
                
                # region float
                case "float":
                    content_frame.grid_columnconfigure(1, weight=1)

                    value = element.text or ""
                    value = value.strip()

                    ctk.CTkLabel(content_frame, text="Value: ", anchor="e").grid(column=0, row=0, sticky="nsew")
                    entry = ctk.CTkEntry(
                        content_frame, width=40, height=40, validate="key",
                        validatecommand=(self.root.register(lambda value: value.replace(".", "", 1).isdigit() or value == ""), '%P')
                    )
                    entry.insert("end", value)
                    entry.bind("<Return>", lambda _: self.root.focus())
                    entry.bind("<Control-s>", lambda _: self.root.focus())
                    entry.bind("<FocusOut>", lambda event, name=element.attrib['name']: self._update_float_value(tree=tree, name=name, event=event))
                    entry.grid(column=1, row=0, sticky="ew", padx=(0, self.Constants.ENTRY_INNER_PADDING))
                
                # region string
                case "string":
                    content_frame.grid_columnconfigure(1, weight=1)

                    value = element.text or ""
                    value = value.strip()

                    ctk.CTkLabel(content_frame, text="Value: ", anchor="e").grid(column=0, row=0, sticky="nsew")
                    entry = ctk.CTkEntry(
                        content_frame, width=40, height=40
                    )
                    entry.insert("end", value)
                    entry.bind("<Return>", lambda _: self.root.focus())
                    entry.bind("<Control-s>", lambda _: self.root.focus())
                    entry.bind("<FocusOut>", lambda event, name=element.attrib['name']: self._update_string_value(tree=tree, name=name, event=event))
                    entry.grid(column=1, row=0, sticky="ew", padx=(0, self.Constants.ENTRY_INNER_PADDING))
                
                # region token
                case "token":
                    content_frame.grid_columnconfigure(1, weight=1)
                    
                    value = element.text or ""
                    value = value.strip()

                    ctk.CTkLabel(content_frame, text="Value: ", anchor="e").grid(column=0, row=0, sticky="nsew")
                    entry = ctk.CTkEntry(
                        content_frame, width=40, height=40
                    )
                    entry.insert("end", value)
                    entry.bind("<Return>", lambda _: self.root.focus())
                    entry.bind("<Control-s>", lambda _: self.root.focus())
                    entry.bind("<FocusOut>", lambda event, name=element.attrib['name']: self._update_token_value(tree=tree, name=name, event=event))
                    entry.grid(column=1, row=0, sticky="ew", padx=(0, self.Constants.ENTRY_INNER_PADDING))
            
            # Height is hardcoded for now because it's way faster and it doesn't give any big issues
            # frame.update_idletasks()
            # frame_height: int = frame.winfo_height()
            frame_height: int = 96
            frame.grid_propagate(False)
            frame.configure(width=(container.winfo_width()//2)-self.Constants.ENTRY_GAP, height=frame_height)
    # endregion


    # region functions
    def _get_frame_column(self, i) -> int:
        return i % 2
    
    def _get_frame_row(self, i) -> int:
        return i // 2
    
    def _get_frame_padx(self, i) -> int | tuple[int, int]:
        return (self.Constants.ENTRY_GAP, 0) if self._get_frame_column(i) == 1 else 0
    
    def _get_frame_pady(self, i) -> int | tuple[int, int]:
        return (self.Constants.ENTRY_GAP, 0) if self._get_frame_row(i) >= 1 else 0
    
    def _update_bool_value(self, tree: xml.ElementTree, name: str, value: bool) -> None:
        new_value: str = str(value).lower()
        element = tree.find(f".//*[@name='{name}']")
        if element is None:
            Logger.error(f"Failed to update value for {name}!\nElement not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nElement not found!")
            return

        element.text = new_value
        tree.write(File.GLOBAL_BASIC_SETTINGS)
    
    def _update_int_value(self, tree: xml.ElementTree, name: str, event) -> None:
        new_value: str = str(event.widget.get())

        if not new_value:
            new_value = "0"
            event.widget.delete(0, "end")
            event.widget.insert(0, "0")
        
        element = tree.find(f".//*[@name='{name}']")
        if element is None:
            Logger.error(f"Failed to update value for {name}!\nElement not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nElement not found!")
            return

        element.text = new_value
        tree.write(File.GLOBAL_BASIC_SETTINGS)
    
    def _update_float_value(self, tree: xml.ElementTree, name: str, event) -> None:
        self._update_int_value(tree=tree, name=name, event=event)
    
    def _update_string_value(self, tree: xml.ElementTree, name: str, event) -> None:
        new_value: str = str(event.widget.get())
        
        element = tree.find(f".//*[@name='{name}']")
        if element is None:
            Logger.error(f"Failed to update value for {name}!\nElement not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nElement not found!")
            return

        element.text = new_value
        tree.write(File.GLOBAL_BASIC_SETTINGS)
    
    def _update_token_value(self, tree: xml.ElementTree, name: str, event) -> None:
        self._update_string_value(tree=tree, name=name, event=event)
    
    def _update_vector2_x_value(self, tree: xml.ElementTree, name: str, event) -> None:
        new_value: str = str(event.widget.get())

        if not new_value:
            new_value = "0"
            event.widget.delete(0, "end")
            event.widget.insert(0, "0")
        
        element = tree.find(f".//*[@name='{name}']")
        if element is None:
            Logger.error(f"Failed to update value for {name}!\nElement not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nElement not found!")
            return
        
        x_element = tree.find(f".//*[@name='{name}']")
        if x_element is None:
            Logger.error(f"Failed to update value for {name}!\nX element not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nX element not found!")
            return

        x_element.text = new_value
        tree.write(File.GLOBAL_BASIC_SETTINGS)
    
    def _update_vector2_y_value(self, tree: xml.ElementTree, name: str, event) -> None:
        new_value: str = str(event.widget.get())

        if not new_value:
            new_value = "0"
            event.widget.delete(0, "end")
            event.widget.insert(0, "0")
        
        element = tree.find(f".//*[@name='{name}']")
        if element is None:
            Logger.error(f"Failed to update value for {name}!\nElement not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nElement not found!")
            return
        
        y_element = tree.find(f".//*[@name='{name}']")
        if y_element is None:
            Logger.error(f"Failed to update value for {name}!\nY element not found!", prefix="GlobalBasicSettingsSection._update_boolean_value()")
            showwarning(ProjectData.NAME, f"Failed to update value for {name}!\nY element not found!")
            return

        y_element.text = new_value
        tree.write(File.GLOBAL_BASIC_SETTINGS)
    # endregion