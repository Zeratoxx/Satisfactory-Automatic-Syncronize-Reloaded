import json

from .World import World


class Config:
    def __init__(self, jsonInput: str | None = None):
        if jsonInput is None or jsonInput == "":
            self.last_git_message: str = "game update"
            self.last_use_experimental: bool = False
            self.last_savegame_choice: int = -1
            self.worlds: list[World] = []
        else:
            self.__dict__ = json.loads(jsonInput)

    def toJSON(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=2)
