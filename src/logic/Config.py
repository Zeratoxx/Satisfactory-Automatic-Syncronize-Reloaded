import os

from logic.OS import OS


class Config:
    def __init__(self, os_type: OS.OSType):
        self.check_interval = 2
        self.username = os.getenv("USERNAME") or os.getenv("USER")

        self.os_type = os_type
        if self.os_type == OS.OSType.WINDOWS:
            self.base_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "FactoryGame", "Saved")
            self.executable_name = "FactoryGameEGS.exe"
        elif self.os_type == OS.OSType.LINUX:
            self.base_path = os.path.join(os.path.expanduser("~"), ".local", "share", "FactoryGame", "Saved")
            self.executable_name = "FactoryGame"
        elif self.os_type == OS.OSType.MAC:
            self.base_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "FactoryGame",
                                          "Saved")
            self.executable_name = "FactoryGame"
        else:
            self.base_path = os.path.join(os.path.expanduser("~"), "FactoryGame", "Saved")
            self.executable_name = "FactoryGame"

        self.save_games = "SaveGames"
        self.which_saved = os.path.join(self.save_games, "common")
        self.logs_dir = os.path.join(self.base_path, "Logs")

        # worlds.json liegt beim Script
        self.worlds_file = os.path.join(os.path.dirname(__file__), "worlds.json")
