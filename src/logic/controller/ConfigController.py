import json
import logging
import os

from logic.models import Config, World


class ConfigController:
    class WorldsManager:
        def __init__(self, config: Config):
            self.config = config
            self.worlds = self.config.worlds

        async def save_worlds(self):
            self.config.worlds = self.worlds
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

    def __init__(self, filename: str = "config.json"):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.config: Config | None = None
        self.worlds_manager: ConfigController.WorldsManager = ConfigController.WorldsManager(self.config)
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.config = Config(json.load(f))
            except Exception as e:
                logging.error(f"Fehler beim Laden der Config: {e}")
                self.config = None
        else:
            logging.info(f"Erstellen einer Konfiguration mit Standardwerten...")
            self.config = Config()
            self.save()
            logging.info(f"Konfiguration mit Standardwerten erstellt und gespeichert.")

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Config: {e}")
