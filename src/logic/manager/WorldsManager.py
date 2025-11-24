import logging

from logic.controller import ConfigController
from logic.models import World


class WorldsManager:
    def __init__(self, config_controller: ConfigController):
        self.config_controller = config_controller
        self.worlds = self.config_controller.config.worlds

    async def save_worlds(self):
        self.config_controller.config.worlds = self.worlds
        self.config_controller.save()
        logging.info("Worlds saved to config.json.")

    async def add_world(self, name: str, path: str, description: str = ""):
        if any(w.name == name for w in self.worlds):
            logging.info(f"World '{name}' already exists.")
            return
        world = World(name, path, description=description)
        self.worlds.append(world)
        await self.save_worlds()
        logging.info(f"World '{name}' added at path '{path}'.")

    async def update_world_metadata(self, world: World):
        world.calculate_metadata()
        await self.save_worlds()

    def list_worlds(self):
        return self.worlds
