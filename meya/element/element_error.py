from typing import TYPE_CHECKING
from typing import Optional

if TYPE_CHECKING:
    from meya.core.source_location import SourceLocation


class ElementError(Exception):
    def __init__(
        self, source_location: Optional["SourceLocation"], message: str
    ):
        self.source_location = source_location
        if self.source_location:
            from meya.core.source_registry import SourceRegistry

            self.source_registry = SourceRegistry.current.get()
        self.message = message

    def __str__(self):
        context = self.context()
        if context:
            return "\n".join([self.message, context])
        else:
            return self.message

    def context(self, indent=2):
        if self.source_location:
            spaces = " " * indent
            lines = []
            lines.append(
                f'{spaces}File: "{self.source_location.file_path}",'
                f" line {self.source_location.line + 1}"
            )
            lines.append(
                f"{spaces}{self.source_location.get_line_text(self.source_registry)}"
            )
            if self.source_location.column is not None:
                lines.append(f"{spaces}{' ' * self.source_location.column}^")
            return "\n".join(lines)
        else:
            return ""


class ElementParseError(ElementError):
    pass


class ElementImportError(ElementError):
    pass


class ElementValidationError(ElementError):
    pass


class ElementTemplateError(ElementError):
    pass


class ElementProcessError(ElementError):
    pass
