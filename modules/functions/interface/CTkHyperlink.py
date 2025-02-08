import customtkinter as ctk
import webbrowser


class CTkHyperlink(ctk.CTkLabel):
    color: str | tuple[str, str] = ("#0000EE", "#2fa8ff")
    hover_color: str | tuple[str, str] = ("#0000CC", "#58bbff")

    def __init__(self, master, url: str, text: str | None = None, fg_color: str | tuple[str, str] = "transparent"):
        super().__init__(master, text=text or url, cursor="hand2", fg_color=fg_color, text_color=self.color)

        self.bind("<Button-1>", lambda _: webbrowser.open_new_tab(url))
        self.bind("<Enter>", lambda _: self.configure(text_color=self.hover_color))
        self.bind("<Leave>", lambda _: self.configure(text_color=self.color))
