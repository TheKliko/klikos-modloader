import webbrowser
from pathlib import Path

from modules.info import Help, LICENSES, CONTRIBUTORS, FEATURE_SUGGESTIONS, SPECIAL_THANKS
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules.functions.interface.CTkHyperlink import CTkHyperlink

import customtkinter as ctk


class AboutSection:
    class Constants:
        LICENSES_PER_ROW: int = 3
        LICENSE_GAP: int = 8
        LICENSE_PADDING: int = 8

        ROW_2_PADX: int = 12
        ROW_2_PADY: int = 12


    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        bold: ctk.CTkFont


    container: ctk.CTkScrollableFrame
    widget_data: dict = {}


    def __init__(self, container: ctk.CTkScrollableFrame) -> None:
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
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,24))

        # Banner
        banner_file: Path = (Directory.RESOURCES / "menu" / "about" / "banner").with_suffix(".png")
        if not banner_file.is_file():
            restore_from_meipass(banner_file)
        banner_image = load_image(banner_file, size=(548, 165))

        ctk.CTkLabel(frame, text="", image=banner_image).grid(column=0, row=0, sticky="new")

        # Buttons
        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsew")
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(4, weight=1)

        github_icon: Path = (Directory.RESOURCES / "menu" / "about" / "github").with_suffix(".png")
        if not github_icon.is_file():
            restore_from_meipass(github_icon)
        github_image = load_image(github_icon)

        chat_icon: Path = (Directory.RESOURCES / "menu" / "about" / "chat").with_suffix(".png")
        if not chat_icon.is_file():
            restore_from_meipass(chat_icon)
        chat_image = load_image(chat_icon)

        ctk.CTkButton(buttons, text="View on GitHub", image=github_image, command=lambda: webbrowser.open_new_tab(Help.GITHUB), width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsew")
        ctk.CTkButton(buttons, text="Changelog", image=github_image, command=lambda: webbrowser.open_new_tab(Help.RELEASES), width=1, anchor="w", compound=ctk.LEFT).grid(column=2, row=0, sticky="nsew", padx=(8,0))
        ctk.CTkButton(buttons, text="Join our Discord", image=chat_image, command=lambda: webbrowser.open_new_tab(Help.DISCORD), width=1, anchor="w", compound=ctk.LEFT).grid(column=3, row=0, sticky="nsew", padx=(8,0))
    # endregion

    
    # region content
    def _load_content(self) -> None:
        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        # region licenses
        licenses_container: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        licenses_container.grid(column=0, row=0, sticky="nsew", pady=(0, 24))
        ctk.CTkLabel(licenses_container, text="Licenses", font=self.Fonts.title, anchor="w").grid(column=0, row=0, columnspan=3, sticky="ew")

        for i, license in enumerate(LICENSES):
            license_frame: ctk.CTkFrame = ctk.CTkFrame(licenses_container, cursor="hand2", width=269 if self._get_license_column(i) == 1 else 268)
            license_frame.grid(column=self._get_license_column(i), row=self._get_license_row(i), sticky="nsew", padx=self.Constants.LICENSE_GAP if self._get_license_column(i) == 1 else 0, pady=(self.Constants.LICENSE_GAP, 0) if self._get_license_row(i) > 0 else 0)
            license_frame.bind("<Button-1>", lambda event, url=license["url"]: webbrowser.open_new_tab(url))

            # Info
            name_frame: ctk.CTkFrame = ctk.CTkFrame(license_frame, fg_color="transparent")
            name_frame.grid(column=0, row=0, sticky="nw", padx=self.Constants.LICENSE_PADDING, pady=(self.Constants.LICENSE_PADDING, 0))
            ctk.CTkLabel(name_frame, text=license["name"], font=self.Fonts.bold, anchor="w").grid(column=0, row=0, sticky="nw")
            ctk.CTkLabel(name_frame, text=f"({license["author"]})", anchor="w").grid(column=1, row=0, sticky="nw", padx=(4, 0))
            
            ctk.CTkLabel(license_frame, text=license["type"], anchor="w").grid(column=0, row=1, rowspan=2, sticky="nw", padx=self.Constants.LICENSE_PADDING, pady=(0, self.Constants.LICENSE_PADDING))

            # If I don't do this then the frame shrink to fit it's content, even though it worked just fine everywhere else ¯\_(ツ)_/¯
            license_frame.grid_propagate(True)
            license_frame.update_idletasks()

            required_height = license_frame.winfo_reqheight()
            license_frame.grid_propagate(False)
            license_frame.configure(height=required_height)

            # Make sure it's clickable when clicking on one of the labels instead of the frame itself
            for widget in license_frame.winfo_children():
                widget.configure(cursor="hand2")
                widget.bind("<Button-1>", lambda event, url=license["url"]: webbrowser.open_new_tab(url))
            for widget in name_frame.winfo_children():
                widget.configure(cursor="hand2")
                widget.bind("<Button-1>", lambda event, url=license["url"]: webbrowser.open_new_tab(url))
        # endregion


        row_2_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        row_2_frame.grid(column=0, row=1, sticky="nsew", pady=(0, 24))

        # region contributors
        if CONTRIBUTORS:
            contributors_container: ctk.CTkFrame = ctk.CTkFrame(row_2_frame, fg_color="transparent")
            contributors_container.grid(column=0, row=0, sticky="w")
            ctk.CTkLabel(contributors_container, text="Contributors", font=self.Fonts.title, anchor="w").grid(column=0, row=0, columnspan=3, sticky="w")

            contributors_frame: ctk.CTkFrame = ctk.CTkFrame(contributors_container, width=268)
            contributors_frame.grid(column=0, row=1, sticky="w", pady=(8,0))

            total_contributors: int = len(CONTRIBUTORS)
            for i, contributor in enumerate(CONTRIBUTORS):
                text: str | None = contributor.get("text")
                if not text:
                    continue
                url: str | None = contributor.get("url")
                
                if url:
                    hyperlink: CTkHyperlink = CTkHyperlink(contributors_frame, url, text=text)
                    hyperlink.grid(column=0, row=i, sticky="w", padx=self.Constants.ROW_2_PADX, pady=self.Constants.ROW_2_PADY if total_contributors == 1 else (self.Constants.ROW_2_PADY,0) if i == 0 else (0,self.Constants.ROW_2_PADY) if i == total_contributors-1 else 0)
                else:
                    label = ctk.CTkLabel(contributors_frame, text=text)
                    label.grid(column=0, row=i, sticky="w", padx=self.Constants.ROW_2_PADX, pady=self.Constants.ROW_2_PADY if total_contributors == 1 else (self.Constants.ROW_2_PADY,0) if i == 0 else (0,self.Constants.ROW_2_PADY) if i == total_contributors-1 else 0)
            
            contributors_frame.grid_propagate(True)
            contributors_frame.update_idletasks()

            required_height = contributors_frame.winfo_reqheight()
            contributors_frame.grid_propagate(False)
            contributors_frame.configure(height=required_height)
        # endregion

        # region feature suggestions
        if FEATURE_SUGGESTIONS:
            feature_suggestions_container: ctk.CTkFrame = ctk.CTkFrame(row_2_frame, fg_color="transparent")
            feature_suggestions_container.grid(column=1, row=0, sticky="w", padx=(8, 0) if CONTRIBUTORS else 0)
            ctk.CTkLabel(feature_suggestions_container, text="Feature Suggestions", font=self.Fonts.title, anchor="w").grid(column=0, row=0, columnspan=3, sticky="w")

            feature_suggestions_frame: ctk.CTkFrame = ctk.CTkFrame(feature_suggestions_container, width=269)
            feature_suggestions_frame.grid(column=0, row=1, sticky="w", pady=(8,0))

            total_feature_suggestions: int = len(FEATURE_SUGGESTIONS)
            for i, feature_suggestion in enumerate(FEATURE_SUGGESTIONS):
                text = feature_suggestion.get("text")
                if not text:
                    continue
                url = feature_suggestion.get("url")
                
                if url:
                    hyperlink = CTkHyperlink(feature_suggestions_frame, url, text=text)
                    hyperlink.grid(column=0, row=i, sticky="w", padx=self.Constants.ROW_2_PADX, pady=self.Constants.ROW_2_PADY if total_feature_suggestions == 1 else (self.Constants.ROW_2_PADY,0) if i == 0 else (0,self.Constants.ROW_2_PADY) if i == total_feature_suggestions-1 else 0)
                else:
                    label = ctk.CTkLabel(feature_suggestions_frame, text=text)
                    label.grid(column=0, row=i, sticky="w", padx=self.Constants.ROW_2_PADX, pady=self.Constants.ROW_2_PADY if total_feature_suggestions == 1 else (self.Constants.ROW_2_PADY,0) if i == 0 else (0,self.Constants.ROW_2_PADY) if i == total_feature_suggestions-1 else 0)
            
            feature_suggestions_frame.grid_propagate(True)
            feature_suggestions_frame.update_idletasks()

            required_height = feature_suggestions_frame.winfo_reqheight()
            feature_suggestions_frame.grid_propagate(False)
            feature_suggestions_frame.configure(height=required_height)

        # region special thanks
        if SPECIAL_THANKS:
            special_thanks_container: ctk.CTkFrame = ctk.CTkFrame(row_2_frame, fg_color="transparent")
            special_thanks_container.grid(column=2, row=0, sticky="w", padx=(8, 0) if (CONTRIBUTORS or SPECIAL_THANKS) else 0)
            ctk.CTkLabel(special_thanks_container, text="Special thanks", font=self.Fonts.title, anchor="w").grid(column=0, row=0, columnspan=3, sticky="w")

            special_thanks_frame: ctk.CTkFrame = ctk.CTkFrame(special_thanks_container, width=268)
            special_thanks_frame.grid(column=0, row=1, sticky="w", pady=(8,0))

            total_special_thanks: int = len(SPECIAL_THANKS)
            for i, item in enumerate(SPECIAL_THANKS):
                text = item.get("text")
                if not text:
                    continue
                url = item.get("url")
                
                if url:
                    hyperlink = CTkHyperlink(special_thanks_frame, url, text=text)
                    hyperlink.grid(column=0, row=i, sticky="w", padx=self.Constants.ROW_2_PADX, pady=self.Constants.ROW_2_PADY if total_special_thanks == 1 else (self.Constants.ROW_2_PADY,0) if i == 0 else (0,self.Constants.ROW_2_PADY) if i == total_special_thanks-1 else 0)
                else:
                    label = ctk.CTkLabel(special_thanks_frame, text=text)
                    label.grid(column=0, row=i, sticky="w", padx=self.Constants.ROW_2_PADX, pady=self.Constants.ROW_2_PADY if total_special_thanks == 1 else (self.Constants.ROW_2_PADY,0) if i == 0 else (0,self.Constants.ROW_2_PADY) if i == total_special_thanks-1 else 0)
            
            special_thanks_frame.grid_propagate(True)
            special_thanks_frame.update_idletasks()

            required_height = special_thanks_frame.winfo_reqheight()
            special_thanks_frame.grid_propagate(False)
            special_thanks_frame.configure(height=required_height)
        # endregion
    # endregion


    # region functions
    def _get_license_column(self, i: int) -> int:
        return i % self.Constants.LICENSES_PER_ROW


    def _get_license_row(self, i: int) -> int:
        return (i // self.Constants.LICENSES_PER_ROW) + 1
    # endregion