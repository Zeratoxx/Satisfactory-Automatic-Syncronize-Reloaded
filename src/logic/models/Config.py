import json
from io import TextIOWrapper

from .World import World


class Config:
    def __init__(self, json_input: TextIOWrapper | None = None):
        if json_input is None:
            self.last_git_message: str = "game update"
            self.last_use_experimental: bool = False
            self.last_savegame_choice: int = -1
            self.worlds: list[World] = []
        else:
            self.__dict__ = json.load(json_input)

    def get(self, key):
        return self.__dict__.get(key, None)

    def set(self, key, value):
        self.__dict__[key] = value
