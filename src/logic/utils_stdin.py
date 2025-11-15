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
