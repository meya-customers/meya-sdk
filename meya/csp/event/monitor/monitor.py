from dataclasses import dataclass
from meya.csp.event import CspEvent
from meya.csp.event.monitor.error import MonitorErrorEvent
from meya.entry.field import entry_field
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class MonitorEvent(CspEvent):
    data: Optional[Dict[str, Any]] = entry_field()
    csp_integration_id: str = entry_field()
    note: Optional[str] = entry_field()

    def create_error(self) -> MonitorErrorEvent:
        return MonitorErrorEvent(
            user_id=self.user_id,
            thread_id=self.thread_id,
            integration_id=self.integration_id,
        )
