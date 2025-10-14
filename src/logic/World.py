from pathlib import Path


class World:
    def __init__(self, name: str, path: str | Path):
        self.name: str = name
        try:
            self.sanitized_folder_path: Path = Path(path).resolve(strict=True)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"At creating world entry for \"{name}\": filepath \"{path}\" was not found!\n" + str(e))
