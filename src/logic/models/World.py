import asyncio
import json
import logging
import os
import shutil
from datetime import datetime
from typing import Any

from pydantic import BaseModel, model_validator
import git


class World(BaseModel):
    name: str
    path: str
    created_at: str = datetime.now().isoformat(timespec="seconds")
    last_played: str | None = None
    save_count: int = 0
    size_mb: float = 0.0
    description: str = ""

    def model_post_init(self, context: Any) -> None:
        if self.path is None:
            raise ValueError(f"World '{self.name}' hat keinen gültigen Pfad in worlds.json!")

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
        return json.loads(self.toJSON())

    def toJSON(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=2)

    @staticmethod
    def from_dict(data: dict, base_path: str = None):
        path = data.get("path")
        if path is None and base_path is not None:
            path = os.path.join(base_path, data["name"])
        return World(
            name=data["name"],
            path=path,
            created_at=data.get("created_at"),
            last_played=data.get("last_played"),
            save_count=data.get("save_count", 0),
            size_mb=data.get("size_mb", 0.0),
            description=data.get("description", "")
        )

    def __repr__(self):
        return f"World(name={self.name}, path={self.path}, saves={self.save_count}, size={self.size_mb}MB)"

    def update(self):
        git_repo = git.Repo(self.path)
        git_repo.git.pull()

    def upload(self, git_message):
        git_repo = git.Repo(self.path)
        git_repo.index.add([self.path])
        git_repo.index.commit(git_message)
        git_repo.git.push()
