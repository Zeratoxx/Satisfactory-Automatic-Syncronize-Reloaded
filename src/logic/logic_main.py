import logging
import asyncio

from logic.models.Config import Config
from logic.controller.ConfigController import ConfigController
from logic.manager.WorldManager import WorldManager
from logic.utils.menu import menu
from logic.models.OS import OS


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    cfg_mgr = ConfigController("config.json")
    cfg = Config(OS().detect_os())
    logging.info(f"Detected OS: {cfg.os_type}")
    manager = WorldManager(cfg_mgr)
    await manager.load_worlds()
    await menu(manager, cfg_mgr, cfg)


if __name__ == "__main__":
    asyncio.run(main())
