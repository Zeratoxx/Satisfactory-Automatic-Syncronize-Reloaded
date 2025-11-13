import os
import platform
import subprocess
import shutil
import time

# --- Betriebssystem-Erkennung ---
def get_os_type():
    system = platform.system().lower()
    if "windows" in system:
        return "Windows"
    elif "linux" in system:
        return "Linux"
    elif "darwin" in system:  # macOS
        return "Mac"
    else:
        return "Unknown"

OS_TYPE = get_os_type()
print(f"Detected OS: {OS_TYPE}")

# --- Variablen ---
checkInterval = 2
useExperimental = False
exeName = "FactoryGameEGS.exe"
gitMessageFile = "gitMessage.txt"
username = os.getenv("USERNAME") or os.getenv("USER")
PATHTOSAVED = os.path.join(os.path.expanduser("~"), "AppData", "Local", "FactoryGame", "Saved")
keepDirInSaved = "blueprints"
saveGames = "SaveGames"
whichSaved = os.path.join(saveGames, "common")
nameOfWorldlistFile = "listOfWorlds.txt"
saveChoiceFile = "lastChoice.txt"
saveWorldChoiceFile = "lastWorldChoice.txt"
searchVal = "rejected"

# --- Hilfsfunktionen ---
def run_command(cmd):
    """Führt einen Shell-Befehl aus und gibt die Ausgabe zurück."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running command {cmd}: {e}")
        return ""

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --- Beispiel: Datei prüfen ---
if not os.path.exists(os.path.join(PATHTOSAVED, nameOfWorldlistFile)):
    print(f"Cannot find {nameOfWorldlistFile}. Please set it up correctly.")
    exit(1)

# --- Beispiel: Git Pull ---
def git_pull(repo_path):
    if os.path.exists(os.path.join(repo_path, ".git")):
        print("Pulling latest changes...")
        run_command("git pull")
    else:
        print("This is not a git repository. Cannot pull.")

# --- Beispiel: Spiel starten ---
def start_game(useExperimental):
    if OS_TYPE == "Windows":
        if not useExperimental:
            run_command('start com.epicgames.launcher://apps/CrabEA?action=launch')
        else:
            run_command('start com.epicgames.launcher://apps/CrabTest?action=launch')
    elif OS_TYPE in ["Linux", "Mac"]:
        print("Game start not implemented for this OS – please adapt manually.")

# --- Beispiel: Prozess überwachen ---
def check_if_running(exeName):
    if OS_TYPE == "Windows":
        while True:
            tasks = run_command(f'tasklist /FI "IMAGENAME eq {exeName}"')
            if exeName in tasks:
                print("Satisfactory is running!")
                time.sleep(checkInterval)
            else:
                print("Satisfactory has been closed! Starting to synchronize...")
                break
    else:
        print("Process monitoring not implemented for non-Windows systems.")

# --- Beispiel: Synchronisation ---
def sync_saves(repo_path):
    print(f"Working with {os.path.join(PATHTOSAVED, whichSaved)} ...")
    ensure_dir(os.path.join(PATHTOSAVED, whichSaved))
    # Kopieren der Savegames
    for file in os.listdir(repo_path):
        if file.endswith(".sav"):
            shutil.copy(os.path.join(repo_path, file), os.path.join(PATHTOSAVED, whichSaved))
    print("Savegames synchronized.")

# --- Hauptablauf ---
def main():
    print("Starting script...")
    repo_path = os.path.join(PATHTOSAVED, "exampleRepo")  # Platzhalter
    git_pull(repo_path)
    start_game(useExperimental)
    check_if_running(exeName)
    sync_saves(repo_path)
    print("Complete. Closing...")

if __name__ == "__main__":
    main()
