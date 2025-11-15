import asyncio
import logging

from git import Repo, GitCommandError


async def git_pull(repo_path: str):
    try:
        repo = await asyncio.to_thread(Repo, repo_path)
        origin = repo.remotes.origin
        await asyncio.to_thread(origin.pull)
        logging.info("Git pull successful.")
    except Exception as e:
        logging.error(f"Git pull failed (is this a git repo?): {e}")


async def git_commit_and_push(repo_path: str, message: str):
    try:
        repo = await asyncio.to_thread(Repo, repo_path)
        await asyncio.to_thread(repo.git.add, A=True)
        await asyncio.to_thread(repo.index.commit, message)
        origin = repo.remotes.origin
        await asyncio.to_thread(origin.push)
        logging.info("Git commit & push successful.")
    except GitCommandError as e:
        logging.error(f"Git command error: {e}")
    except Exception as e:
        logging.error(f"Git commit/push failed (is this a git repo?): {e}")
