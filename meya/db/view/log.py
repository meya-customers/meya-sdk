import sys
import traceback

from dataclasses import dataclass
from dataclasses import field
from meya.core.source_location import SourceLocation
from meya.log.entry import LogEntry
from meya.log.entry.exception import LogExceptionEntry
from meya.log.entry.message import LogMessageEntry
from meya.log.level import Level
from meya.log.scope import Scope
from meya.time import get_milliseconds_timestamp
from meya.util.context_var import ScopedContextVar
from meya.util.dict import to_dict
from typing import ClassVar
from typing import List
from typing import cast


@dataclass
class LogView:
    entries: List[LogEntry] = field(default_factory=list)
    source_location: SourceLocation = field(default=None)

    current: ClassVar = cast(ScopedContextVar["LogView"], ScopedContextVar())

    def debug(self, message, *args, scope=Scope.BOT, context=None):
        self._log(Level.DEBUG, message, scope, context, *args)

    def info(self, message, *args, scope=Scope.BOT, context=None):
        self._log(Level.INFO, message, scope, context, *args)

    def warning(self, message, *args, scope=Scope.BOT, context=None):
        self._log(Level.WARNING, message, scope, context, *args)

    def error(self, message, *args, scope=Scope.BOT, context=None):
        self._log(Level.ERROR, message, scope, context, *args)

    def exception(self, scope=Scope.BOT, context=None):
        context = {**self._base_context, **(context or {})}
        exc_type, exc_value, exc_traceback = sys.exc_info()
        stack_trace = list(
            map(
                lambda f: [f.filename, str(f.lineno), f.name, f.line],
                traceback.extract_tb(exc_traceback),
            )
        )
        self._append(
            LogExceptionEntry(
                context=context,
                exception=str(exc_value),
                exception_type=str(exc_type),
                scope=scope,
                stack_trace=stack_trace,
                timestamp=get_milliseconds_timestamp(),
            )
        )

    @property
    def _base_context(self):
        def build():
            if self.source_location:
                yield {"source_location": to_dict(self.source_location)}

        context = {}
        for context_item in build():
            context = {**context, **context_item}
        return context

    def _log(self, level, message, scope, context, *args):
        context = {**self._base_context, **(context or {})}
        args = to_dict(list(args))

        # create an entry and append to the list
        entry = LogMessageEntry(
            args=args,
            context=context,
            level=level,
            message=message,
            scope=scope,
            timestamp=get_milliseconds_timestamp(),
        )
        self._append(entry)

    def _append(self, entry: LogEntry) -> None:
        self.entries.append(entry)
