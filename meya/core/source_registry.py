from dataclasses import dataclass
from meya.app_config import AppConfig
from meya.core.source import Source
from meya.util.context_var import ScopedContextVar
from meya.util.pathspec import make_pathspec
from meya.util.pathspec import read_gitignore_lines
from meya.util.pathspec import read_meyaignore_lines
from meya.util.pathspec import subtract_pathspec
from meya.util.pathspec import walk_pathspec
from os import path
from typing import ClassVar
from typing import List
from typing import cast


@dataclass
class SourceRegistry:
    items: List[Source]

    current: ClassVar = cast(
        ScopedContextVar["SourceRegistry"], ScopedContextVar()
    )

    def text(self, file_path: str):
        for item in self.items:
            if item.file_path == file_path:
                return item.text
        raise Exception(f'File not found "{file_path}"')

    @classmethod
    def find_and_read(cls, app_config: AppConfig) -> "SourceRegistry":
        items = []
        pathspec = subtract_pathspec(
            pathspec=make_pathspec(
                [
                    "*.yaml",
                    "*.yml",
                    "!.*",
                    "!config.*.yaml",
                    "!config.yaml",
                    "!vault.*.yaml",
                    "!vault.yaml",
                ]
            ),
            ignore_pathspec=make_pathspec(
                [*read_gitignore_lines(), *read_meyaignore_lines()]
            ),
        )
        file_paths = walk_pathspec(app_config.package_path, pathspec)
        for file_path in file_paths:
            with file_path.open("r", encoding="utf-8") as file:
                items.append(
                    Source(path.normpath(str(file_path)), file.read())
                )
        return cls(
            items=list(sorted(items, key=lambda source: source.file_path))
        )
