from modules import Logger

import customtkinter as ctk


class FontImportWindow(ctk.CTkTopLevel):
    root: ctk.CTk
    

    def __init__(self, root: ctk.CTk, *args, **kwargs) -> None:
        self.root = root
        self.super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.withdraw()
        # Hide window immediately after it's created. Only show it when needed
    

    def show(self) -> None:
        raise NotImplementedError("Function not implemented!")
        # show window,
        # position it in the center of root

        # idk

        # finally: hide window
    
        self.deiconify()
        self.geometry(self._get_geometry())

        try:
            pass

        except Exception as e:
            Logger.error(f"Something went wrong when creating font mod! {type(e).__name__}: {e}")

        finally:
            self._hide()


    def _get_geometry(self) -> str:
        root_geometry: str = self.root.winfo_geometry()
        root_size, root_x, root_y = root_geometry.split("+")
        root_width, root_height = map(int, root_size.split("x"))

        self.update_idletasks()
        width: int = self.winfo_width()
        height: int = self.winfo_height()

        x: int = int(root_x) + ((root_width - width) // 2)
        y: int = int(root_y) + ((root_height - height) // 2)

        return f"{width}x{height}+{x}+{y}"
    

    def _hide(self) -> None:
        self.withdraw()