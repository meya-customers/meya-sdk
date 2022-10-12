from dataclasses import dataclass
from meya.csp.event import CspEvent
from meya.csp.event.session.agent.request.error import AgentRequestErrorEvent
from meya.entry.field import entry_field
from numbers import Real
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class AgentRequestEvent(CspEvent):
    data: Optional[Dict[str, Any]] = entry_field()
    csp_integration_id: str = entry_field()
    note: Optional[str] = entry_field()
    timeout: Real = entry_field()
    timeout_flow: Optional[str] = entry_field()  # TODO Change to trigger

    def create_error(self) -> AgentRequestErrorEvent:
        return AgentRequestErrorEvent(
            user_id=self.user_id,
            thread_id=self.thread_id,
            integration_id=self.integration_id,
        )
