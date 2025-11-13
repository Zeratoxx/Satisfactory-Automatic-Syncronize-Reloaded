import os
import platform
import shutil
import subprocess
import time
import zipfile
import logging
import psutil
import enum

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
    git_message_file = "gitMessage.txt"
    username = os.getenv("USERNAME") or os.getenv("USER")
    base_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "FactoryGame", "Saved")
    keep_dir = "blueprints"
    save_games = "SaveGames"
    which_saved = os.path.join(save_games, "common")
    world_list_file = "listOfWorlds.txt"
    save_choice_file = "lastChoice.txt"
    save_world_choice_file = "lastWorldChoice.txt"
    logs_dir = os.path.join(base_path, "Logs")

# --- Hilfsfunktionen ---
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def run_git_command(repo_path: str, command: list[str]):
    if os.path.exists(os.path.join(repo_path, ".git")):
        try:
            subprocess.run(["git"] + command, cwd=repo_path, check=True)
            logging.info(f"Git {' '.join(command)} executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Git command failed: {e}")
    else:
        logging.warning("Not a git repository.")

def copy_saves(src: str, dst: str):
    ensure_dir(dst)
    for file in os.listdir(src):
        if file.endswith(".sav"):
            shutil.copy(os.path.join(src, file), dst)
    logging.info("Savegames copied.")

def compress_saves(src: str, zip_path: str):
    ensure_dir(os.path.dirname(zip_path))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src):
            for file in files:
                if file.endswith(".sav"):
                    zf.write(os.path.join(root, file), arcname=file)
    logging.info("Savegames compressed into zip.")

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
    cfg = Config()
    repo_path = os.path.join(cfg.base_path, "exampleRepo")  # Platzhalter

    # Git aktualisieren
    run_git_command(repo_path, ["pull"])

    # Spiel starten
    use_experimental = False  # hier könnte man Eingabe abfragen
    start_game(use_experimental, OS_TYPE)

    # Warten bis Spiel beendet
    wait_for_game(cfg.exe_name, cfg.check_interval)

    # Synchronisation
    copy_saves(repo_path, os.path.join(cfg.base_path, cfg.which_saved))
    compress_saves(os.path.join(cfg.base_path, cfg.which_saved),
                   os.path.join(repo_path, "savpackage.zip"))

    # Git commit & push
    run_git_command(repo_path, ["add", "."])
    run_git_command(repo_path, ["commit", "-m", f"Spielupdate {cfg.username}"])
    run_git_command(repo_path, ["push"])

    logging.info("Complete. Closing...")

if __name__ == "__main__":
    main()
