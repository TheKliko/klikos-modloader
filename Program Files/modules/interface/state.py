import ctypes


def hide() -> None:
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )


def show() -> None:
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 9 )


def focus() -> None:
    show()
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.SetForegroundWindow(hwnd)