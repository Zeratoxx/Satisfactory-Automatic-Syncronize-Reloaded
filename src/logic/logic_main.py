import logging
import asyncio

from logic.controller import ConfigController, RunController
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
    menu(config_controller, run_controller)


if __name__ == "__main__":
    asyncio.run(main())
