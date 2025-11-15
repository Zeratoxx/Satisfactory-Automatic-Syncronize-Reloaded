import asyncio
import logging
import os

import psutil

from logic.OSType import OSType


async def start_game(use_experimental: bool, os_type: OSType):
    if os_type == OSType.WINDOWS:
        app = "CrabTest" if use_experimental else "CrabEA"
        logging.info(f"Starting game via Epic Launcher: {app}")
        await asyncio.to_thread(os.system, f"start com.epicgames.launcher://apps/{app}?action=launch")
    elif os_type == OSType.LINUX:
        logging.info("Linux detected. Please start the game manually (Epic Launcher via Wine/Proton).")
    elif os_type == OSType.MAC:
        logging.info("macOS detected. Please start the game manually (Epic Launcher for Mac).")
    else:
        logging.error("Unsupported OS type.")


async def wait_for_game(exe_name: str, interval: int):
    started = False
    while True:
        running = await asyncio.to_thread(lambda: any(p.name() == exe_name for p in psutil.process_iter()))
        if running:
            if not started:
                logging.info("Game started.")
                started = True
            await asyncio.sleep(interval)
        else:
            if started:
                logging.info("Game closed. Synchronizing saves...")
                break
            else:
                logging.info("Game not yet started...")
                await asyncio.sleep(interval)
