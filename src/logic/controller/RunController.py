import os
import asyncio
import logging
import shutil

import psutil

from logic.models import OS, World, GitRepository


class RunController:
    def __init__(self, check_interval: int = 2, debug: bool = False):
        if not debug:
            home_folder = os.path.expanduser("~")
        else:
            home_folder = os.getcwd()
        self.os_type: OS.OSType = OS().detect_os()
        if self.os_type == OS.OSType.WINDOWS:
            base_path: str = os.path.join(home_folder, "AppData", "Local", "FactoryGame", "Saved")
            self.executable_name: str = "FactoryGameEGS.exe"
        elif self.os_type == OS.OSType.LINUX:
            base_path: str = os.path.join(home_folder, ".local", "share", "FactoryGame", "Saved")
            self.executable_name: str = "FactoryGame"
        elif self.os_type == OS.OSType.MAC:
            base_path: str = os.path.join(home_folder, "Library", "Application Support", "FactoryGame",
                                          "Saved")
            self.executable_name: str = "FactoryGame"
        else:
            base_path: str = os.path.join(home_folder, "FactoryGame", "Saved")
            self.executable_name: str = "FactoryGame"

        if debug:
            os.makedirs(base_path, exist_ok=True)
        self.game_data_path: str = base_path
        self.savegames_path: str = os.path.join(base_path, "SaveGames")
        self.common_savegames_path: str = os.path.join(self.savegames_path, "common")
        self.backup_savegame_path: str = self.savegames_path + "-bak"
        self.logs_path: str = os.path.join(base_path, "logs")

        self.username: str = os.getenv("USERNAME") or os.getenv("USER")
        self.check_interval: int = check_interval
        self.glob_anti_sav_files = "!([.]sav)"

    def _backup_current_savegame_path(self):
        logging.info("Backing up current savegame path.")
        shutil.copytree(self.savegames_path, self.backup_savegame_path,
                        ignore=shutil.ignore_patterns(self.glob_anti_sav_files), dirs_exist_ok=True)
        logging.info("Backup done.")

    def _clean_up_savegames_folder(self):
        self._backup_current_savegame_path()
        shutil.rmtree(self.common_savegames_path)
        for file in os.listdir(self.savegames_path):
            if file.endswith(".sav"):
                os.remove(file)

    def _load_world(self, world: World):
        self._clean_up_savegames_folder()
        world.update()
        shutil.copytree(world.path, self.common_savegames_path, ignore=shutil.ignore_patterns(self.glob_anti_sav_files),
                        dirs_exist_ok=True)

    async def load_world_and_start_game(self, world: World, use_experimental: bool):
        self._load_world(world)
        if self.os_type == OS.OSType.WINDOWS:
            app = "CrabTest" if use_experimental else "CrabEA"
            logging.info(f"Starting game via Epic Launcher: {app}")
            await asyncio.to_thread(os.system, f"start com.epicgames.launcher://apps/{app}?action=launch")
        elif self.os_type == OS.OSType.LINUX:
            logging.info("Linux detected. Please start the game manually (Epic Launcher via Wine/Proton).")
        elif self.os_type == OS.OSType.MAC:
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

    def save_world(self, world: World, git_message: str):
        shutil.copytree(self.savegames_path, world.path, ignore=shutil.ignore_patterns(self.glob_anti_sav_files),
                        dirs_exist_ok=True)
        world.upload(git_message)
