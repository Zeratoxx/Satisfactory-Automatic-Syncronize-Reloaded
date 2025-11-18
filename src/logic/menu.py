import logging
import os

from git import Repo

from logic.Config import Config
from logic.ConfigManager import ConfigManager
from logic.utils_stdin import prompt, prompt_with_default, timed_input
from logic.WorldManager import WorldManager
from logic.RunController import RunController
from logic.GitRepository import GitRepository


async def menu(manager: WorldManager, cfg_mgr: ConfigManager, cfg: Config):
    while True:
        print("\n=== Welt-Manager Menü ===")
        print("1) Neue Welt hinzufügen")
        print("2) Bestehende Welt auswählen und starten")
        print("3) Welt bearbeiten")
        print("4) Welt löschen")
        print("5) Git-Message bearbeiten")
        print("6) Beenden")
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

            last_world = cfg_mgr.get_setting("last_world")
            if last_world:
                print(f"Letzte Auswahl war: {last_world}")

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

            cfg_mgr.set_setting("last_world", chosen_world.name)

            # Experimental-Flag
            last_exp = cfg_mgr.get_setting("last_experimental", False)
            print(f"Letzte Einstellung: {'Experimental' if last_exp else 'Normal'}")
            exp_raw = input("Experimental-Version starten? (j/n, Enter=letzte Einstellung): ").strip().lower()
            if exp_raw == "j":
                use_experimental = True
            elif exp_raw == "n":
                use_experimental = False
            else:
                use_experimental = last_exp
            cfg_mgr.set_setting("last_experimental", use_experimental)

            logging.info(f"Chosen world: {chosen_world}")





            # TODO REMOVE DEBUG
            last_msg = cfg_mgr.get_setting("last_git_message", "Spielupdate (Standard)")
            print(f"Letzte Git-Message: {last_msg}")

            git_msg = timed_input("Neue Git-Message:", timeout=7, default=last_msg)
            # Basistext in config.json speichern
            cfg_mgr.set_setting("last_git_message", git_msg)
            # Conventional Commit mit Datum/User/Host bauen
            final_msg = GitRepository.build_conventional_commit(git_msg)
            print(final_msg)
            # TODO REMOVE DEBUG





            runner = RunController(cfg)
            # Spiel starten
            await runner.start_game(use_experimental, chosen_world)

            # Warten bis Spiel beendet
            await runner.wait_for_game_closed()

            # Savegames synchronisieren und Metadaten aktualisieren
            destination = os.path.join(cfg.base_path, cfg.which_saved)
            await chosen_world.copy_saves_to(destination)
            await manager.update_world_metadata(chosen_world)

            last_msg = cfg_mgr.get_setting("last_git_message", "Spielupdate (Standard)")
            print(f"Letzte Git-Message: {last_msg}")

            git_msg = timed_input("Neue Git-Message:", timeout=5, default=last_msg)
            # Basistext in config.json speichern
            cfg_mgr.set_setting("last_git_message", git_msg)

            # Conventional Commit mit Datum/User/Host bauen
            final_msg = build_conventional_commit(git_msg, commit_type="update")

            # Nur Basistext speichern
            cfg_mgr.set_setting("last_git_message", git_msg)

            await git_commit_and_push(chosen_world.path, final_msg)
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

            confirm = input(f"Soll die Welt '{chosen_world.name}' wirklich gelöscht werden? (j/n, 'z'=Zurück, 'q'=Beenden): ").strip().lower()
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
        elif choice == "6":
            print("Beende Programm...")
            break

        # --- Git-Message bearbeiten ---
        elif choice == "5":
            last_msg = cfg_mgr.get_setting("last_git_message")
            if last_msg:
                print(f"Aktuelle Git-Message: {last_msg}")
            else:
                print("Noch keine Git-Message gespeichert.")

            new_msg = input("Neue Git-Message eingeben ('z'=Zurück, 'q'=Beenden, Enter=behalten): ").strip()
            if new_msg.lower() == "q":
                print("Beende Programm...")
                break
            if new_msg.lower() == "z":
                continue
            if not new_msg:
                print("Git-Message unverändert.")
                continue

            cfg_mgr.set_setting("last_git_message", new_msg)
            print(f"Neue Git-Message gespeichert: {new_msg}")

        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")
