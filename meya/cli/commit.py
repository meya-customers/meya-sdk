from meya.util.git import Git
from meya.util.system import NonZeroExitCode
from os import path
from typing import Optional

DEFAULT_NAME = "Meya"
DEFAULT_EMAIL = "support@meya.ai"


async def commit_app_workspace(git: Git):
    await git("add", "--all")
    if path.exists(path.join(git.work_tree, "config.yaml")):
        await git("add", "--force", "config.yaml")
    return await commit(git)


async def commit(git: Git, message: str = "."):
    next_revision = await _get_next_revision(git)
    if next_revision:
        index_tree = await git("write-tree", stdout_stripped=True)
        next_revision_tree = await git(
            "show",
            "--no-patch",
            "--format=%T",
            next_revision,
            stdout_stripped=True,
        )
        perform_commit = index_tree != next_revision_tree
    else:
        perform_commit = True
    if perform_commit:
        author_args = []
        try:
            await git("config", "--get", "user.name")
            await git("config", "--get", "user.email")
        except NonZeroExitCode:
            author_args = ["--author", f"{DEFAULT_NAME} <{DEFAULT_EMAIL}>"]

        await git(
            "commit",
            "--allow-empty",
            "--message",
            message,
            *author_args,
            stdout_stripped=True,
        )
        next_revision = await _get_next_revision(git)
    return next_revision


async def get_current_revision(git) -> Optional[str]:
    return await _get_revision(git, "HEAD")


async def get_current_branch(git) -> Optional[str]:
    return await _get_revision(git, "--abbrev-ref", "HEAD")


async def _get_next_revision(git) -> str:
    return await _get_revision(git, "refs/heads/master")


async def _get_revision(git, *args) -> Optional[str]:
    try:
        return await git(
            "rev-parse", "--quiet", "--verify", *args, stdout_stripped=True
        )
    except NonZeroExitCode:
        return None
