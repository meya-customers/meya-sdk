from os import path
from os import walk
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from pathspec.util import normalize_file
from typing import Iterator
from typing import List
from typing import Optional


def make_pathspec(ignore_lines: List[str]) -> PathSpec:
    return PathSpec.from_lines(GitWildMatchPattern, ignore_lines)


def subtract_pathspec(
    *, pathspec: PathSpec, ignore_pathspec: PathSpec
) -> PathSpec:
    return PathSpec(
        [
            *pathspec.patterns,
            *[
                GitWildMatchPattern(pattern.regex, include=False)
                for pattern in ignore_pathspec.patterns
            ],
        ]
    )


def read_gitignore_lines() -> List[str]:
    return [".git", *read_ignore_lines(Path(".gitignore")), "!config.yaml"]


def read_meyaignore_lines() -> List[str]:
    return read_ignore_lines(Path(".meyaignore"))


def read_ignore_lines(ignore_path: Path) -> List[str]:
    if not ignore_path.exists():
        return []
    try:
        with ignore_path.open("r") as ignore_file:
            return ignore_file.read().splitlines(keepends=False)
    except IOError as e:
        print(f"Could not open {ignore_path} file: {e}")
        return []


def match_pathspec(file: str, pathspec: PathSpec) -> Optional[bool]:
    file = normalize_file(file)
    matched = None
    for pattern in pathspec.patterns:
        if pattern.include is not None:
            if file in pattern.match((file,)):
                matched = pattern.include
    return matched


def walk_pathspec(
    base_dir: Path, pathspec: PathSpec, topdown: bool = True
) -> Iterator[Path]:
    for dirpath, dirnames, filenames in walk(str(base_dir), topdown=topdown):
        new_dirnames = []
        for dirname in dirnames:
            full_dirname = path.join(dirpath, dirname)
            match = match_pathspec(full_dirname, pathspec)
            if match is not False:
                new_dirnames.append(dirname)
            if match is True:
                yield Path(full_dirname)
        for filename in filenames:
            full_filename = path.join(dirpath, filename)
            match = match_pathspec(full_filename, pathspec)
            if match is True:
                yield Path(full_filename)
        dirnames[:] = new_dirnames
