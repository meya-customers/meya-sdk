import os
import subprocess

from asyncio import Future
from dataclasses import dataclass
from meya.util.system import system
from os import makedirs
from os import path
from typing import Optional
from typing import Tuple
from typing import Union
from urllib.parse import quote_plus
from urllib.parse import urlparse
from urllib.parse import urlunparse

MEYA_DIR = ".v2"
GIT_DIR = path.join(MEYA_DIR, "git")
MEYA_GIT_REMOTE = "origin"
MEYA_GIT_BRANCH = "master"


@dataclass
class Git:
    git_dir: str
    work_tree: Optional[str]
    git_args: Tuple[str, ...]

    async def __call__(
        self, *args, **kwargs
    ) -> Union[None, str, bytes, Tuple[subprocess.Popen, Future]]:
        return await system(*self.git_args, *args, **kwargs)

    @classmethod
    async def init_shadow(cls, sub_directory=".") -> "Git":
        git_dir = cls.shadow_directory(sub_directory)
        return await cls.init(git_dir, sub_directory)

    @classmethod
    def has_shadow(cls, sub_directory=".") -> bool:
        git_dir = cls.shadow_directory(sub_directory)
        return path.exists(git_dir)

    @staticmethod
    def shadow_directory(sub_directory) -> str:
        return path.join(sub_directory, GIT_DIR)

    @classmethod
    async def init(
        cls,
        git_dir: str = ".git",
        work_tree: Optional[str] = ".",
        initial_branch: str = MEYA_GIT_BRANCH,
    ) -> "Git":
        git_args = (
            "git",
            "--git-dir",
            git_dir,
            *(("--work-tree", work_tree) if work_tree else ()),
        )
        git = Git(git_dir, work_tree, git_args)
        makedirs(git_dir, exist_ok=True)
        if work_tree:
            makedirs(work_tree, exist_ok=True)
        if not os.listdir(git_dir):
            await git(
                "init",
                *(() if work_tree else ("--bare",)),
                "--initial-branch",
                initial_branch,
                stdout_stripped=True,
            )
        await git("config", "http.version", "HTTP/1.1")
        return git

    @staticmethod
    def basic_auth_url(remote_url: str, username: str, password: str) -> str:
        remote_parts = urlparse(remote_url)
        return urlunparse(
            remote_parts._replace(
                netloc=f"{quote_plus(username)}:{quote_plus(password)}@{remote_parts.netloc}"
            )
        )

    async def add_remote(
        self,
        remote_name: str,
        remote_url: str,
        username: str,
        password: str,
        use_credential_helper: bool = False,
    ) -> None:
        if not use_credential_helper:
            remote_url = self.basic_auth_url(remote_url, username, password)
        else:
            await self.set_credentials(remote_url, username, password)
        await self("remote", "add", remote_name, remote_url)

    async def set_credentials(
        self, remote_url: str, username: str, password: str
    ) -> None:
        auth_url = self.basic_auth_url(remote_url, username, password)
        credentials_file_path = path.join(
            path.abspath(self.git_dir), "git-credentials"
        )
        with open(credentials_file_path, "w+") as credentials_file:
            credentials_file.write(auth_url)
        await self(
            "config",
            "credential.helper",
            f"store --file {credentials_file_path}",
        )

    async def remove_remote(self, remote_name: str) -> None:
        await self("remote", "remove", remote_name)

    async def set_user(self, name: str, email: str) -> None:
        await self("config", "user.name", name or email)
        await self("config", "user.email", email)

    async def set_upstream(
        self, remote_name: str, *args, branch: str = MEYA_GIT_BRANCH
    ) -> None:
        await self.push(remote_name, "--set-upstream", *args, branch=branch)

    async def push(
        self, remote_name: str, *args, branch: str = MEYA_GIT_BRANCH
    ) -> None:
        await self("push", *args, remote_name, branch)

    async def fetch(
        self,
        remote_name: str,
        *args,
        branch: str = MEYA_GIT_BRANCH,
        shallow: bool = False,
        treeless: bool = False,
    ) -> None:
        if shallow:
            args = (
                "--depth",
                "1",
                *args,
            )
        if treeless:
            # NOTE: The filter is to avoid downloading unneeded data from Git,
            # but is not currently supported by Gogs (as of 0.11.86)
            args = (
                "--filter",
                "tree:0",
                *args,
            )
        await self("fetch", *args, remote_name, branch)

    async def pull(
        self, remote_name: str, *args, branch: str = MEYA_GIT_BRANCH
    ) -> None:
        await self("pull", *args, remote_name, branch)

    async def head(self, remote: str) -> str:
        git_info = await self("ls-remote", remote, "HEAD", stdout_text=True)
        return git_info[:40]


async def _git_cat_file_hash_and_contents(git, next_revision, path):
    git_info = await git(
        "cat-file",
        "--batch=%(objectname)",
        stdin=f"{next_revision}:{path}",
        stdout_text=True,
    )
    file_hash = git_info[:40]
    assert git_info[40] == "\n", f"git cat-file error {git_info}"
    file_contents = git_info[41:]
    return file_hash, file_contents


async def _git_cat_file_contents(git, next_revision, path):
    return await git(
        "show", f"{next_revision}:{path}", stdout_text=True, stderr=False
    )


async def _git_cat_file_hash(git, next_revision, path):
    return await git(
        "cat-file",
        "--batch-check=%(objectname)",
        stdin=f"{next_revision}:{path}",
        stdout_stripped=True,
    )
