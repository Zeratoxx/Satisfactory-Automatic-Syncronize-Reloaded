import logging
import asyncio

from logic.controller import ConfigController, RunController
from logic.manager import WorldsManager
from logic.utils import menu


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    config_controller = ConfigController()
    run_controller = RunController()
    logging.info(f"Detected OS: {run_controller.os_type}")
    manager = WorldsManager(cfg_mgr)
    await manager.load_worlds()
    await menu(manager, cfg_mgr, cfg)


if __name__ == "__main__":
    asyncio.run(main())
