import logging
import asyncio

from logic.Config import Config
from logic.WorldManager import WorldManager
from logic.menu import menu
from logic.os_utils import detect_os


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    cfg = Config(detect_os())
    logging.info(f"Detected OS: {cfg.os_type}")
    manager = WorldManager(cfg)
    await manager.load_worlds()
    await menu(manager, cfg)


if __name__ == "__main__":
    asyncio.run(main())
