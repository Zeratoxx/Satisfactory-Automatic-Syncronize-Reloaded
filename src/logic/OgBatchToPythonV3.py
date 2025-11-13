import os
import shutil
import logging
import enum
import platform
import psutil
import subprocess
import time
import json

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


# --- Enum für OS Types ---
class OSType(enum.Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC = "Mac"
    UNKNOWN = "Unknown"


def detect_os() -> OSType:
    system = platform.system().lower()
    if "windows" in system:
        return OSType.WINDOWS
    elif "linux" in system:
        return OSType.LINUX
    elif "darwin" in system:  # macOS
        return OSType.MAC
    else:
        return OSType.UNKNOWN


OS_TYPE = detect_os()
logging.info(f"Detected OS: {OS_TYPE.value}")


# --- Konfiguration ---
class Config:
    check_interval = 2
    exe_name = "FactoryGameEGS.exe"
    username = os.getenv("USERNAME") or os.getenv("USER")
    base_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "FactoryGame", "Saved")
    save_games = "SaveGames"
    which_saved = os.path.join(save_games, "common")
    logs_dir = os.path.join(base_path, "Logs")
    worlds_file = os.path.join(base_path, "worlds.json")  # formatierte JSON


# --- World-Klasse ---
class World:
    def __init__(self, name: str, base_path: str):
        self.name = name.strip()
        self.path = os.path.join(base_path, self.name)

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    def list_files(self) -> list[str]:
        if not self.exists():
            return []
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    def list_saves(self) -> list[str]:
        return [f for f in self.list_files() if f.endswith(".sav")]

    def copy_saves_to(self, destination: str):
        os.makedirs(destination, exist_ok=True)
        for save in self.list_saves():
            src = os.path.join(self.path, save)
            dst = os.path.join(destination, save)
            shutil.copy(src, dst)
        logging.info(f"Copied {len(self.list_saves())} saves from world '{self.name}' to {destination}")

    def to_dict(self) -> dict:
        return {"name": self.name}

    @staticmethod
    def from_dict(data: dict, base_path: str):
        return World(data["name"], base_path)

    def __repr__(self):
        return f"World(name={self.name})"


# --- WorldManager-Klasse ---
class WorldManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.worlds: list[World] = []

    def load_worlds(self):
        """Lädt Welten aus JSON-Datei."""
        if not os.path.exists(self.cfg.worlds_file):
            logging.warning("No worlds database file found. Starting empty.")
            self.worlds = []
            return
        with open(self.cfg.worlds_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.worlds = [World.from_dict(w, self.cfg.base_path) for w in data]
        logging.info(f"Loaded {len(self.worlds)} worlds from database.")

    def save_worlds(self):
        """Speichert Welten in formatierter JSON-Datei."""
        with open(self.cfg.worlds_file, "w", encoding="utf-8") as f:
            json.dump([w.to_dict() for w in self.worlds], f, indent=2)  # formatierte Ausgabe
        logging.info("Worlds saved to database (formatted JSON).")

    def add_world(self, name: str):
        """Neue Welt hinzufügen."""
        world = World(name, self.cfg.base_path)
        if all(w.name != name for w in self.worlds):
            self.worlds.append(world)
            self.save_worlds()
            logging.info(f"World '{name}' added.")
        else:
            logging.info(f"World '{name}' already exists.")

    def list_worlds(self):
        return self.worlds


# --- Hilfsfunktionen ---
def wait_for_game(exe_name: str, interval: int):
    started = False
    while True:
        running = any(p.name() == exe_name for p in psutil.process_iter())
        if running:
            if not started:
                logging.info("Game started.")
                started = True
            time.sleep(interval)
        else:
            if started:
                logging.info("Game closed. Synchronizing saves...")
                break
            else:
                logging.info("Game not yet started...")
                time.sleep(interval)


def start_game(use_experimental: bool, os_type: OSType):
    if os_type == OSType.WINDOWS:
        app = "CrabTest" if use_experimental else "CrabEA"
        logging.info(f"Starting game via Epic Launcher: {app}")
        subprocess.run(["start", f"com.epicgames.launcher://apps/{app}?action=launch"], shell=True)
    elif os_type == OSType.LINUX:
        logging.warning("Game start not implemented for Linux. Use Wine/Proton manually.")
    elif os_type == OSType.MAC:
        logging.warning("Game start not implemented for macOS. Use Epic Launcher for Mac.")
    else:
        logging.error("Unsupported OS type.")


# --- Hauptablauf ---
def main():
    cfg = Config()
    manager = WorldManager(cfg)

    # Welten laden
    manager.load_worlds()
    logging.info(f"Available worlds: {manager.list_worlds()}")

    # Beispiel: Neue Welt hinzufügen
    manager.add_world("TestWorld")

    # Beispiel: Erste Welt auswählen
    if manager.worlds:
        chosen_world = manager.worlds[0]
        logging.info(f"Chosen world: {chosen_world}")

        # Spiel starten
        use_experimental = False
        start_game(use_experimental, OS_TYPE)

        # Warten bis Spiel beendet
        wait_for_game(cfg.exe_name, cfg.check_interval)

        # Savegames synchronisieren
        destination = os.path.join(cfg.base_path, cfg.which_saved)
        chosen_world.copy_saves_to(destination)

    logging.info("Complete. Closing...")


if __name__ == "__main__":
    main()
