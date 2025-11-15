import os
import shutil
import logging
import enum
import platform
import psutil
import asyncio
import json
from datetime import datetime
from git import Repo, GitCommandError

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
            self.executable_name = "FactoryGameEGS.exe"
        elif os_type == OSType.LINUX:
            self.base_path = os.path.join(os.path.expanduser("~"), ".local", "share", "FactoryGame", "Saved")
            self.executable_name = "FactoryGame"
        elif os_type == OSType.MAC:
            self.base_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "FactoryGame",
                                          "Saved")
            self.executable_name = "FactoryGame"
        else:
            self.base_path = os.path.join(os.path.expanduser("~"), "FactoryGame", "Saved")
            self.executable_name = "FactoryGame"

        self.save_games = "SaveGames"
        self.which_saved = os.path.join(self.save_games, "common")
        self.logs_dir = os.path.join(self.base_path, "Logs")

        # worlds.json liegt beim Script
        self.worlds_file = os.path.join(os.path.dirname(__file__), "worlds.json")


# --- World-Klasse ---
class World:
    def __init__(self, name: str, path: str,
                 created_at: str = None,
                 last_played: str = None,
                 save_count: int = 0,
                 size_mb: float = 0.0,
                 description: str = ""):
        self.name = name.strip()
        if path is None:
            raise ValueError(f"World '{name}' hat keinen gültigen Pfad in worlds.json!")
        self.path = path.strip()
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.last_played = last_played
        self.save_count = save_count
        self.size_mb = size_mb
        self.description = description

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    def list_saves(self) -> list[str]:
        if not self.exists():
            return []
        return [f for f in os.listdir(self.path) if f.endswith(".sav")]

    def calculate_metadata(self):
        saves = self.list_saves()
        self.save_count = len(saves)
        total_size = 0
        for f in saves:
            try:
                total_size += os.path.getsize(os.path.join(self.path, f))
            except FileNotFoundError:
                continue
        self.size_mb = round(total_size / (1024 * 1024), 2)
        self.last_played = datetime.now().isoformat(timespec="seconds")

    async def copy_saves_to(self, destination: str):
        os.makedirs(destination, exist_ok=True)
        for save in self.list_saves():
            src = os.path.join(self.path, save)
            dst = os.path.join(destination, save)
            await asyncio.to_thread(shutil.copy, src, dst)
        self.calculate_metadata()
        logging.info(f"Copied {self.save_count} saves ({self.size_mb} MB) from world '{self.name}' to {destination}")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "created_at": self.created_at,
            "last_played": self.last_played,
            "save_count": self.save_count,
            "size_mb": self.size_mb,
            "description": self.description
        }

    @staticmethod
    def from_dict(data: dict, base_path: str = None):
        path = data.get("path")
        if path is None and base_path is not None:
            path = os.path.join(base_path, data["name"])
        return World(
            data["name"],
            path,
            created_at=data.get("created_at"),
            last_played=data.get("last_played"),
            save_count=data.get("save_count", 0),
            size_mb=data.get("size_mb", 0.0),
            description=data.get("description", "")
        )

    def __repr__(self):
        return f"World(name={self.name}, path={self.path}, saves={self.save_count}, size={self.size_mb}MB)"


# --- WorldManager ---
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


# --- Git Funktionen ---
async def git_pull(repo_path: str):
    try:
        repo = await asyncio.to_thread(Repo, repo_path)
        origin = repo.remotes.origin
        await asyncio.to_thread(origin.pull)
        logging.info("Git pull successful.")
    except Exception as e:
        logging.error(f"Git pull failed (is this a git repo?): {e}")


async def git_commit_and_push(repo_path: str, message: str):
    try:
        repo = await asyncio.to_thread(Repo, repo_path)
        await asyncio.to_thread(repo.git.add, A=True)
        await asyncio.to_thread(repo.index.commit, message)
        origin = repo.remotes.origin
        await asyncio.to_thread(origin.push)
        logging.info("Git commit & push successful.")
    except GitCommandError as e:
        logging.error(f"Git command error: {e}")
    except Exception as e:
        logging.error(f"Git commit/push failed (is this a git repo?): {e}")


# --- OS-spezifische Funktionen ---
async def start_game(use_experimental: bool, os_type: OSType):
    if os_type == OSType.WINDOWS:
        app = "CrabTest" if use_experimental else "CrabEA"
        logging.info(f"Starting game via Epic Launcher: {app}")
        await asyncio.to_thread(os.system, f"start com.epicgames.launcher://apps/{app}?action=launch")
    elif os_type == OSType.LINUX:
        logging.info("Linux detected. Please start the game manually (Epic Launcher via Wine/Proton).")
    elif os_type == OSType.MAC:
        logging.info("macOS detected. Please start the game manually (Epic Launcher for Mac).")
    else:
        logging.error("Unsupported OS type.")


async def wait_for_game(exe_name: str, interval: int):
    started = False
    while True:
        running = await asyncio.to_thread(lambda: any(p.name() == exe_name for p in psutil.process_iter()))
        if running:
            if not started:
                logging.info("Game started.")
                started = True
            await asyncio.sleep(interval)
        else:
            if started:
                logging.info("Game closed. Synchronizing saves...")
                break
            else:
                logging.info("Game not yet started...")
                await asyncio.sleep(interval)


# --- Hilfsfunktionen für Eingaben ---
def prompt(text: str, allow_quit: bool = True) -> str:
    """Einfache Prompt-Funktion. 'q' beendet das Programm sofort, wenn allow_quit=True."""
    val = input(text).strip()
    if allow_quit and val.lower() == "q":
        print("Beende Programm...")
        raise SystemExit
    return val


def prompt_with_default(label: str, current: str, allow_quit: bool = True) -> str:
    """Gibt aktuellen Wert an, leere Eingabe bedeutet 'behalten'."""
    val = input(f"{label} [{current}]: ").strip()
    if allow_quit and val.lower() == "q":
        print("Beende Programm...")
        raise SystemExit
    return val if val else current


# --- Menüsystem ---
async def menu(manager: WorldManager, cfg: Config):
    while True:
        print("\n=== Welt-Manager Menü ===")
        print("1) Neue Welt hinzufügen")
        print("2) Bestehende Welt auswählen und starten")
        print("3) Welt bearbeiten (Änderungen werden NACH Bestätigung gespeichert)")
        print("4) Welt löschen")
        print("5) Beenden")
        print("Hinweis: 'z' = Zurück ins Hauptmenü, 'q' = Sofort beenden")

        choice = input("Bitte Auswahl eingeben: ").strip().lower()
        if choice == "q":
            print("Beende Programm...")
            break

        # --- Neue Welt hinzufügen ---
        if choice == "1":
            try:
                name = prompt("Name der neuen Welt: ")
                desc = prompt("Beschreibung (optional): ")
                path = prompt("Pfad zum Speicherort der Welt (Ordner mit .sav-Dateien): ")

                if not os.path.exists(path):
                    create = prompt("Pfad existiert nicht. Ordner anlegen? (j/n): ").lower()
                    if create == "j":
                        os.makedirs(path, exist_ok=True)
                        print(f"Ordner erstellt: {path}")
                    else:
                        print("Welt wurde nicht hinzugefügt (Pfad existiert nicht).")
                        continue

                await manager.add_world(name, path, description=desc)
                print(f"Welt '{name}' wurde hinzugefügt.")
            except SystemExit:
                break

        # --- Welt auswählen und starten ---
        elif choice == "2":
            worlds = manager.list_worlds()
            if not worlds:
                print("Keine Welten vorhanden. Bitte zuerst eine Welt hinzufügen.")
                continue

            print("\nVerfügbare Welten:")
            for idx, w in enumerate(worlds, start=1):
                print(f"{idx}) {w.name} | Pfad: {w.path} | Saves: {w.save_count} | Größe: {w.size_mb} MB")

            sel_raw = input("Nummer der Welt auswählen ('z'=Zurück, 'q'=Beenden): ").strip().lower()
            if sel_raw == "q":
                print("Beende Programm...")
                break
            if sel_raw == "z":
                continue

            try:
                sel = int(sel_raw)
                chosen_world = worlds[sel - 1]
            except (ValueError, IndexError):
                print("Ungültige Auswahl.")
                continue

            logging.info(f"Chosen world: {chosen_world}")

            # Git Pull (falls Repo)
            await git_pull(chosen_world.path)

            # Spiel starten
            use_experimental = False
            await start_game(use_experimental, OS_TYPE)

            # Warten bis Spiel beendet
            await wait_for_game(cfg.executable_name, cfg.check_interval)

            # Savegames synchronisieren und Metadaten aktualisieren
            destination = os.path.join(cfg.base_path, cfg.which_saved)
            await chosen_world.copy_saves_to(destination)
            await manager.update_world_metadata(chosen_world)

            # Git Commit & Push (falls Repo)
            await git_commit_and_push(chosen_world.path, f"Spielupdate {cfg.username} ({chosen_world.last_played})")

            logging.info("Welt-Synchronisation abgeschlossen.")

        # --- Welt bearbeiten ---
        elif choice == "3":
            worlds = manager.list_worlds()
            if not worlds:
                print("Keine Welten vorhanden.")
                continue

            print("\nVerfügbare Welten:")
            for idx, w in enumerate(worlds, start=1):
                print(f"{idx}) {w.name} | Pfad: {w.path}")

            sel_raw = input("Nummer der Welt zum Bearbeiten ('z'=Zurück, 'q'=Beenden): ").strip().lower()
            if sel_raw == "q":
                print("Beende Programm...")
                break
            if sel_raw == "z":
                continue

            try:
                sel = int(sel_raw)
                chosen_world = worlds[sel - 1]
            except (ValueError, IndexError):
                print("Ungültige Auswahl.")
                continue

            print("\nBearbeiten (leerlassen = behalten, 'q'=Beenden):")
            try:
                new_name = prompt_with_default("Neuer Name", chosen_world.name)
                new_path = prompt_with_default("Neuer Pfad", chosen_world.path)
                new_desc = prompt_with_default("Neue Beschreibung", chosen_world.description)
            except SystemExit:
                break

            print("\nÄnderungen zur Bestätigung:")
            print(f"Name: {chosen_world.name} -> {new_name}")
            print(f"Pfad: {chosen_world.path} -> {new_path}")
            print(f"Beschreibung: {chosen_world.description} -> {new_desc}")
            confirm = input("Änderungen speichern? (j/n, 'z'=Zurück, 'q'=Beenden): ").strip().lower()
            if confirm == "q":
                print("Beende Programm...")
                break
            if confirm == "z" or confirm != "j":
                print("Bearbeiten abgebrochen. Keine Änderungen gespeichert.")
                continue

            chosen_world.name = new_name
            chosen_world.path = new_path
            chosen_world.description = new_desc
            await manager.save_worlds()
            print("Änderungen gespeichert.")

        # --- Welt löschen ---
        elif choice == "4":
            worlds = manager.list_worlds()
            if not worlds:
                print("Keine Welten vorhanden.")
                continue

            print("\nVerfügbare Welten:")
            for idx, w in enumerate(worlds, start=1):
                print(f"{idx}) {w.name} | Pfad: {w.path}")

            sel_raw = input("Nummer der Welt zum Löschen ('z'=Zurück, 'q'=Beenden): ").strip().lower()
            if sel_raw == "q":
                print("Beende Programm...")
                break
            if sel_raw == "z":
                continue

            try:
                sel = int(sel_raw)
                chosen_world = worlds[sel - 1]
            except (ValueError, IndexError):
                print("Ungültige Auswahl.")
                continue

            confirm = input(
                f"Soll die Welt '{chosen_world.name}' wirklich gelöscht werden? (j/n, 'z'=Zurück, 'q'=Beenden): ").strip().lower()
            if confirm == "q":
                print("Beende Programm...")
                break
            if confirm == "z" or confirm != "j":
                print("Löschen abgebrochen.")
                continue

            manager.worlds.remove(chosen_world)
            await manager.save_worlds()
            print(f"Welt '{chosen_world.name}' wurde gelöscht.")

        # --- Beenden ---
        elif choice == "5":
            print("Beende Programm...")
            break

        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")


# --- Hauptablauf ---
async def main():
    cfg = Config(OS_TYPE)
    manager = WorldManager(cfg)
    await manager.load_worlds()
    await menu(manager, cfg)


if __name__ == "__main__":
    asyncio.run(main())
