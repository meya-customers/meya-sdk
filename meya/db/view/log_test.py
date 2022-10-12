import sys

from dataclasses import dataclass
from meya.db.view.log import LogView
from meya.log.entry import LogEntry
from meya.log.entry.message import LogMessageEntry
from meya.log.scope import Scope


@dataclass
class MockLogView(LogView):
    def exception(self, scope=Scope.SYSTEM, context=None):
        # Raise the exception instead of logging it
        _, exc_value, _ = sys.exc_info()
        raise exc_value

    def _append(self, entry: LogEntry) -> None:
        if isinstance(entry, LogMessageEntry):
            print(entry.message, entry.args, entry.context)
        super()._append(entry)
