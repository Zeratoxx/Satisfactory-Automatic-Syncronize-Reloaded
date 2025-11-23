import logging

from logic.controller.ConfigController import ConfigController
from logic.models.World import World


class WorldsManager:
    def __init__(self, cfg_mgr: ConfigController):
        self.cfg_mgr = cfg_mgr
        self.worlds: list[World] = []

    async def load_worlds(self):
        data = self.cfg_mgr.get_worlds()
        self.worlds = [World.from_dict(w) for w in data]
        logging.info(f"Loaded {len(self.worlds)} worlds from config.json.")

    async def save_worlds(self):
        self.cfg_mgr.set_worlds([w.to_dict() for w in self.worlds])
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
