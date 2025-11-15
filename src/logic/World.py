import asyncio
import logging
import os
import shutil
from datetime import datetime


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
