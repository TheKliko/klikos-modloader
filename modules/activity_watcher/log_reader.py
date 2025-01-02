from typing import Literal


class LogReader:
    _last_status: dict = {}
    _current_status: dict = {}
    _should_update_status: bool = False
    mode: Literal["Player", "Studio"]


    def __init__(self, mode: Literal["Player", "Studio"]):
        self.mode = mode