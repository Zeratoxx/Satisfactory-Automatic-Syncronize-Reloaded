import os
import asyncio
import logging

import psutil

from logic.Config import Config
from logic.OSType import OSType
from logic.World import World


class RunController:
    def __init__(self, cfg: Config):
        self.os_type: OSType = cfg.os_type
        self.executable_name = cfg.executable_name
        self.savegame_path: str = cfg.base_path
        self.backup_savegame_path: str = cfg.base_path + "-bak"
        self.check_interval: int = cfg.check_interval

    def _backup_current_savegame_path(self):
        logging.info("Backing up current savegame path.")
        os.copy_file_range(self.savegame_path, self.backup_savegame_path)
        logging.info("Backup done.")

    def _load_world(self, world: World):
        self._backup_current_savegame_path()
        os.remove(self.savegame_path)
        os.copy_file_range(world.sanitized_folder_path, self.savegame_path)

    async def start_game(self, world: World, use_experimental: bool):
        self._load_world(world)
        if self.os_type == OSType.WINDOWS:
            app = "CrabTest" if use_experimental else "CrabEA"
            logging.info(f"Starting game via Epic Launcher: {app}")
            await asyncio.to_thread(os.system, f"start com.epicgames.launcher://apps/{app}?action=launch")
        elif self.os_type == OSType.LINUX:
            logging.info("Linux detected. Please start the game manually (Epic Launcher via Wine/Proton).")
        elif self.os_type == OSType.MAC:
            logging.info("macOS detected. Please start the game manually (Epic Launcher for Mac).")
        else:
            logging.error("Unsupported OS type.")

    async def wait_for_game_closed(self):
        started = False
        while True:
            running = await asyncio.to_thread(
                lambda: any(p.name() == self.executable_name for p in psutil.process_iter()))
            if running:
                if not started:
                    logging.info("Game started.")
                    started = True
                await asyncio.sleep(self.check_interval)
            else:
                if started:
                    logging.info("Game closed. Synchronizing saves...")
                    break
                else:
                    logging.info("Game not yet started...")
                    await asyncio.sleep(self.check_interval)
