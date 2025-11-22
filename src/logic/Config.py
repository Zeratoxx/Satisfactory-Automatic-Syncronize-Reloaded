from logic import World


class Config:
    def __init__(self):
        self.last_savegame_choice: int = -1
        self.last_use_experimental: bool = False
        self.last_git_message: str = "game update"
        self.worlds: list[World] = []
