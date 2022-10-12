from dataclasses import dataclass
from meya.component.element import Component
from meya.csp.event.session.agent.request import AgentRequestEvent
from meya.csp.integration import CspIntegrationRef
from meya.element.field import element_field
from meya.entry import Entry
from meya.text.event.say import SayEvent
from typing import List
from typing import Optional


@dataclass
class AgentRequestComponent(Component):
    say: Optional[str] = element_field(default=None)
    integration: CspIntegrationRef = element_field()
    note: Optional[str] = element_field(default=None)
    timeout: Optional[int] = element_field(
        default=60
    )  # TODO Pick a field name that doesn't conflict with base element timeout
    timeout_flow: Optional[str] = element_field(
        default=None
    )  # TODO Change to trigger
    data: Optional[dict] = element_field(default=None)

    async def start(self) -> List[Entry]:
        events = []
        if self.say:
            events.append(SayEvent(text=self.say))
        events.append(
            AgentRequestEvent(
                data=self.data,
                csp_integration_id=self.integration.ref,
                note=self.note,
                timeout=float(self.timeout),
                timeout_flow=self.timeout_flow,
            )
        )
        return self.respond(*events)
