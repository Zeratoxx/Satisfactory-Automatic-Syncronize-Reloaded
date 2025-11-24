import logging
import asyncio

from logic.models import Config, OS
from logic.controller import ConfigController
from logic.manager import WorldsManager
from logic.utils import menu


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    cfg_mgr = ConfigController("config.json")
    cfg = Config(OS().detect_os())
    logging.info(f"Detected OS: {cfg.os_type}")
    manager = WorldsManager(cfg_mgr)
    await manager.load_worlds()
    await menu(manager, cfg_mgr, cfg)


if __name__ == "__main__":
    asyncio.run(main())
