import threading
import queue
import sys
import time



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


def timed_input(prompt: str, timeout: int, default: str) -> str:
    print(f"{prompt} (Timeout={timeout}s, Enter=letzte/Standard verwenden)")
    print(f"Automatisch genutzt falls keine Eingabe: {default}")

    q = queue.Queue()

    def reader():
        try:
            inp = sys.stdin.readline()
            q.put(inp.strip())
        except Exception:
            q.put("")

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    start = time.time()
    while True:
        try:
            return q.get(timeout=timeout - (time.time() - start)) or default
        except queue.Empty:
            print(f"\nTimeout erreicht, nutze: {default}")
            return default
