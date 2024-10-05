import webbrowser


def open_in_browser(url: str) -> None:
    webbrowser.open_new_tab(url=url)