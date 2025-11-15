import asyncio
import json
import logging
import os

from logic.Config import Config
from logic.World import World


class WorldManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.worlds: list[World] = []

    async def load_worlds(self):
        if not os.path.exists(self.cfg.worlds_file):
            logging.warning("No worlds database file found. Creating new one.")
            await self.save_worlds()  # schreibt []
            return
        data = await asyncio.to_thread(self._read_json)
        # Fallback: base_path nur verwenden, wenn path fehlt (für alte JSONs)
        self.worlds = [World.from_dict(w, base_path=self.cfg.base_path) for w in data]
        logging.info(f"Loaded {len(self.worlds)} worlds from database.")

    async def save_worlds(self):
        await asyncio.to_thread(self._write_json, [w.to_dict() for w in self.worlds])
        logging.info("Worlds saved to database (formatted JSON).")

    def _read_json(self):
        with open(self.cfg.worlds_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, data):
        os.makedirs(os.path.dirname(self.cfg.worlds_file), exist_ok=True)
        with open(self.cfg.worlds_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

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
