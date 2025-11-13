import os
import shutil
import logging
import enum
import platform
import psutil
import time
import json
from git import Repo, GitCommandError  # GitPython

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
    def __init__(self, os_type: OSType):
        self.check_interval = 2
        self.username = os.getenv("USERNAME") or os.getenv("USER")

        if os_type == OSType.WINDOWS:
            self.base_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "FactoryGame", "Saved")
            self.exe_name = "FactoryGameEGS.exe"
        elif os_type == OSType.LINUX:
            self.base_path = os.path.join(os.path.expanduser("~"), ".local", "share", "FactoryGame", "Saved")
            self.exe_name = "FactoryGame"
        elif os_type == OSType.MAC:
            self.base_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "FactoryGame",
                                          "Saved")
            self.exe_name = "FactoryGame"
        else:
            self.base_path = os.path.join(os.path.expanduser("~"), "FactoryGame", "Saved")
            self.exe_name = "FactoryGame"

        self.save_games = "SaveGames"
        self.which_saved = os.path.join(self.save_games, "common")
        self.logs_dir = os.path.join(self.base_path, "Logs")
        self.worlds_file = os.path.join(self.base_path, "worlds.json")


# --- World-Klasse ---
class World:
    def __init__(self, name: str, base_path: str):
        self.name = name.strip()
        self.path = os.path.join(base_path, self.name)

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    def list_saves(self) -> list[str]:
        if not self.exists():
            return []
        return [f for f in os.listdir(self.path) if f.endswith(".sav")]

    def copy_saves_to(self, destination: str):
        os.makedirs(destination, exist_ok=True)
        for save in self.list_saves():
            shutil.copy(os.path.join(self.path, save), destination)
        logging.info(f"Copied {len(self.list_saves())} saves from world '{self.name}' to {destination}")

    def to_dict(self) -> dict:
        return {"name": self.name}

    @staticmethod
    def from_dict(data: dict, base_path: str):
        return World(data["name"], base_path)

    def __repr__(self):
        return f"World(name={self.name})"


# --- WorldManager ---
class WorldManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.worlds: list[World] = []

    def load_worlds(self):
        if not os.path.exists(self.cfg.worlds_file):
            logging.warning("No worlds database file found. Starting empty.")
            self.worlds = []
            return
        with open(self.cfg.worlds_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.worlds = [World.from_dict(w, self.cfg.base_path) for w in data]
        logging.info(f"Loaded {len(self.worlds)} worlds from database.")

    def save_worlds(self):
        with open(self.cfg.worlds_file, "w", encoding="utf-8") as f:
            json.dump([w.to_dict() for w in self.worlds], f, indent=2)
        logging.info("Worlds saved to database (formatted JSON).")

    def add_world(self, name: str):
        world = World(name, self.cfg.base_path)
        if all(w.name != name for w in self.worlds):
            self.worlds.append(world)
            self.save_worlds()
            logging.info(f"World '{name}' added.")
        else:
            logging.info(f"World '{name}' already exists.")

    def list_worlds(self):
        return self.worlds


# --- Git Funktionen mit GitPython ---
def git_pull(repo_path: str):
    try:
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        logging.info("Git pull successful.")
    except Exception as e:
        logging.error(f"Git pull failed: {e}")


def git_commit_and_push(repo_path: str, message: str):
    try:
        repo = Repo(repo_path)
        repo.git.add(A=True)
        repo.index.commit(message)
        origin = repo.remotes.origin
        origin.push()
        logging.info("Git commit & push successful.")
    except GitCommandError as e:
        logging.error(f"Git command error: {e}")
    except Exception as e:
        logging.error(f"Git commit/push failed: {e}")


# --- OS-spezifische Funktionen ---
def start_game(use_experimental: bool, os_type: OSType):
    if os_type == OSType.WINDOWS:
        app = "CrabTest" if use_experimental else "CrabEA"
        logging.info(f"Starting game via Epic Launcher: {app}")
        subprocess.run(["start", f"com.epicgames.launcher://apps/{app}?action=launch"], shell=True)
    elif os_type == OSType.LINUX:
        logging.info("Linux detected. Please start the game manually (Epic Launcher via Wine/Proton).")
    elif os_type == OSType.MAC:
        logging.info("macOS detected. Please start the game manually (Epic Launcher for Mac).")
    else:
        logging.error("Unsupported OS type.")


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


# --- Hauptablauf ---
def main():
    cfg = Config(OS_TYPE)
    manager = WorldManager(cfg)
    manager.load_worlds()

    if not manager.worlds:
        logging.warning("No worlds found in database.")
        return

    chosen_world = manager.worlds[0]
    logging.info(f"Chosen world: {chosen_world.name}")

    # Git Pull
    git_pull(chosen_world.path)

    # Spiel starten
    use_experimental = False
    start_game(use_experimental, OS_TYPE)

    # Warten bis Spiel beendet
    wait_for_game(cfg.exe_name, cfg.check_interval)

    # Savegames synchronisieren
    destination = os.path.join(cfg.base_path, cfg.which_saved)
    chosen_world.copy_saves_to(destination)

    # Git Commit & Push
    git_commit_and_push(chosen_world.path, f"Spielupdate {cfg.username}")

    logging.info("Complete. Closing...")


if __name__ == "__main__":
    main()
