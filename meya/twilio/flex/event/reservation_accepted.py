from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event


@dataclass
class TwilioFlexReservationAcceptedEvent(Event):
    agent_name: str = entry_field()
    task_attributes: dict = entry_field()
    worker_attributes: dict = entry_field()
