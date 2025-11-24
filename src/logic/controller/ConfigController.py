import json
import logging
import os

from logic.models import Config


class ConfigController:
    def __init__(self, filename: str = "config.json"):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.config: Config | None = None
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
