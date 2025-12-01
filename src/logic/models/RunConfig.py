from pydantic import BaseModel

from .World import World


class RunConfig(BaseModel):
    last_git_message: str = "game update"
    last_use_experimental: bool = False
    last_savegame_choice_path: str = ""
    worlds: list[World] = []
