import asyncio
import logging

from git import Repo, GitCommandError


class GitRepository:
    def __init__(self, repo: Repo):
        self.repo: Repo = repo

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
