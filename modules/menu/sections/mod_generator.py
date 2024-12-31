import customtkinter as ctk


class ModGeneratorSection:
    class Constants:
        SECTION_TITLE: str = "Mod Generator [BETA]"
        SECTION_DESCRIPTION: str = "This feature is still in development. Expect things to break"
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont


    container: ctk.CTkScrollableFrame


    def __init__(self, container: ctk.CTkScrollableFrame) -> None:
        self.container = container
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)


    def show(self) -> None:
        self._destroy()
        self._load_title()


    def _destroy(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()


    def _load_title(self) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")