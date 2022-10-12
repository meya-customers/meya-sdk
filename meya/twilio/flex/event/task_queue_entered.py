from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event
from meya.twilio.flex.payload.task_router import TaskQueueAssignmentStatus


@dataclass
class TwilioFlexTaskQueueEnteredEvent(Event):
    task_priority: str = entry_field()
    task_assignment_status: TaskQueueAssignmentStatus = entry_field()
    task_attributes: dict = entry_field()
