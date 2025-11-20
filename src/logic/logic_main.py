import logging
import asyncio

from logic.Config import Config
from logic.ConfigManager import ConfigManager
from logic.WorldManager import WorldManager
from logic.menu import menu
from logic.OS import OS


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    cfg_mgr = ConfigManager("config.json")
    cfg = Config(OS().detect_os())
    logging.info(f"Detected OS: {cfg.os_type}")
    manager = WorldManager(cfg_mgr)
    await manager.load_worlds()
    await menu(manager, cfg_mgr, cfg)


if __name__ == "__main__":
    asyncio.run(main())
