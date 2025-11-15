import logging
import os

from logic.Config import Config
from logic.TO_BE_DELETED_stdin_utils import prompt, prompt_with_default
from logic.WorldManager import WorldManager
from logic.game_utils import start_game, wait_for_game
from logic.git_utils import git_pull, git_commit_and_push


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
            await start_game(use_experimental, cfg.os_type)

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

            confirm = (input(
                f"Soll die Welt '{chosen_world.name}' wirklich gelöscht werden? (j/n, 'z'=Zurück, 'q'=Beenden): ")
                       .strip().lower())
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
