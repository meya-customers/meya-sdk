from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional

if TYPE_CHECKING:
    from meya.core.source_registry import SourceRegistry


@dataclass
class SourceLocation:
    file_path: str
    line: int
    column: Optional[int]

    def get_line_text(self, source_registry: "SourceRegistry"):
        file_text = source_registry.text(self.file_path)
        lines = file_text.splitlines()
        if self.line < len(lines):
            return lines[self.line]
        else:
            return ""

    def for_yaml_item(self, obj: list, index: int) -> "SourceLocation":
        from ruamel.yaml.comments import LineCol

        lc = getattr(obj, LineCol.attrib, None)
        if lc is not None:
            [line, column] = lc.data[index]
            return SourceLocation(self.file_path, line, column)
        else:
            return self

    def for_yaml_key(self, obj: dict, key: Any) -> "SourceLocation":
        from ruamel.yaml.comments import LineCol

        lc = getattr(obj, LineCol.attrib, None)
        if lc:
            [line, column, _, _] = lc.data[key]
            return SourceLocation(self.file_path, line, column)
        else:
            return self

    def for_yaml_value(self, obj: dict, key: Any) -> "SourceLocation":
        from ruamel.yaml.comments import LineCol

        lc = getattr(obj, LineCol.attrib, None)
        if lc is not None:
            [_, _, line, column] = lc.data[key]
            return SourceLocation(self.file_path, line, column)
        else:
            return self
