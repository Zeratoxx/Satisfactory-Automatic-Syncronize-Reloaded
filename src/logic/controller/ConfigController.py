import json
import logging
import os

from logic.models import RunConfig, World


class ConfigController:
    def __init__(self, filename: str = "config.json", file_encoding: str = "utf-8"):
        self.file_encoding = file_encoding
        self.filename: str = os.path.join(os.getcwd(), filename)
        self.config: RunConfig | None = None
        self.deserialize_config()

    def deserialize_config(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding=self.file_encoding) as f:
                    data = json.load(f)
                self.config = RunConfig(**data)
            except Exception as e:
                logging.error(f"Error at fetching the config file: {e}")
                self.config = None
        else:
            logging.info(f"Create configuration with default values...")
            self.config = RunConfig()
            self.serialize_config()
            logging.info(f"Configuration with default values created and serialized.")

    def serialize_config(self):
        try:
            with open(self.filename, "w", encoding=self.file_encoding) as f:
                json.dump(self.config,
                          f,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=2)
                logging.info(f"Worlds saved to {self.filename}.")
        except Exception as e:
            logging.error(f"Error at serializing the config: {e}")

    def get_setting(self, key: str, default=None):
        value = self.config.get(key)
        return value if value is not None else default

    def set_setting(self, key: str, value):
        self.config.set(key, value)

    def set_worlds_list(self, worlds: list[World]):
        self.config.worlds = worlds
        self.serialize_config()

    def patch_worlds_list(self, worlds_to_be_updated: list[World]):
        for world_to_be_updated in worlds_to_be_updated:
            for index, world in enumerate(self.config.worlds):
                if world.name == world_to_be_updated.name:
                    self.config.worlds[index] = world_to_be_updated
                    self.serialize_config()
                else:
                    logging.info(f"World '{world.name}' does not exist yet, nothing to patch.")

    def add_world(self, name: str, path: str, description: str = ""):
        if any(w.name == name for w in self.config.worlds):
            logging.info(f"World '{name}' already exists.")
            return
        worlds = self.config.worlds.copy()
        worlds.append(World(name=name, path=path, description=description))
        self.set_worlds_list(worlds)
        logging.info(f"World '{name}' added at path '{path}'.")

    def fetch_world_metadata(self, world: World):
        world.calculate_metadata()
        self.patch_worlds_list([world])

    def remove_world(self, chosen_world: World):
        for world in self.config.worlds:
            if world.name == chosen_world.name:
                self.config.worlds.remove(world)
                self.serialize_config()
            else:
                logging.info(f"World '{world.name}' does not exist, nothing to remove.")

    def get_worlds(self) -> list[World]:
        return self.config.worlds
