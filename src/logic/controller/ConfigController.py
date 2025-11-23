import json
import logging
import os


class ConfigController:
    def __init__(self, filename: str):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                logging.error(f"Fehler beim Laden der Config: {e}")
                self.data = {}
        else:
            self.data = {"settings": {}, "worlds": []}

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Config: {e}")

    # --- Settings ---
    def get_setting(self, key, default=None):
        return self.data.get("settings", {}).get(key, default)

    def set_setting(self, key, value):
        if "settings" not in self.data:
            self.data["settings"] = {}
        self.data["settings"][key] = value
        self.save()

    # --- Worlds ---
    def get_worlds(self):
        return self.data.get("worlds", [])

    def set_worlds(self, worlds):
        self.data["worlds"] = worlds
        self.save()
