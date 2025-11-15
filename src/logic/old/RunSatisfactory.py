import os

from logic.World import World


class RunSatisfactory:
    def __init__(self, os_type: str, savegame_path: str):
        self.os: str = os_type
        self.savegame_path: str = savegame_path
        self.backup_savegame_path: str = savegame_path + "-bak"

    def load_world(self, world: World):
        os.copy_file_range(self.savegame_path, self.backup_savegame_path)
        os.remove(self.savegame_path)
        os.copy_file_range(world.sanitized_folder_path, self.savegame_path)

    async def run(self):
        os.cmd("echo kek")  # TODO everything
