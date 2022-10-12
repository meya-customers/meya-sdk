from dataclasses import dataclass
from meya.component.element import Component
from meya.csp.event.session.end import SessionEndEvent
from meya.csp.integration import CspIntegrationRef
from meya.element.field import element_field
from meya.entry import Entry
from typing import List


@dataclass
class SessionEndComponent(Component):
    integration: CspIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        end_session_event = SessionEndEvent(
            csp_integration_id=self.integration.ref
        )
        return self.respond(end_session_event)
