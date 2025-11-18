import asyncio
import logging
from datetime import datetime, timezone
import socket
import os

from git import Repo, GitCommandError


class GitRepository:
    def __init__(self, repo: Repo):
        self.repo: Repo = repo

    @staticmethod
    def build_conventional_commit(base_message: str, commit_type: str = "update") -> str:
        user = os.environ.get("USERNAME") or os.environ.get("USER")
        host = socket.gethostname()
        # ISO 8601 mit Offset, ohne "Z"
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        return f"{commit_type}({user}): {base_message}\n\n{now} from {host}"

    async def git_pull(self):
        try:
            origin = self.repo.remotes.origin
            await asyncio.to_thread(origin.pull)
            logging.info("Git pull successful.")
        except Exception as e:
            logging.error(f"Git pull failed (is this a git repo?): {e}")

    async def git_commit_and_push(self, message: str):
        try:
            await asyncio.to_thread(self.repo.git.add, A=True)
            await asyncio.to_thread(self.repo.index.commit, message)
            origin = self.repo.remotes.origin
            await asyncio.to_thread(origin.push)
            logging.info("Git commit & push successful.")
        except GitCommandError as e:
            logging.error(f"Git command error: {e}")
        except Exception as e:
            logging.error(f"Git commit/push failed (is this a git repo?): {e}")
