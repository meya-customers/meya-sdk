from dataclasses import dataclass
from meya.component.element import Component
from meya.csp.event.note import NoteEvent
from meya.element.field import element_field
from meya.entry import Entry
from typing import List


@dataclass
class NoteComponent(Component):
    note: str = element_field(
        signature=True,
        help=(
            "Leave a note in the transcript for customer support agents. These notes "
            "will not be sent to the end user and will only be visible to the agent. "
            "Each customer support integration will display bot notes in a different "
            "way, please see the integration documentation for specific details."
        ),
    )

    async def start(self) -> List[Entry]:
        return self.respond(NoteEvent(text=self.note))
