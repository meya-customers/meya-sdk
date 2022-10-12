from dataclasses import dataclass
from meya.util.enum import SimpleEnum


@dataclass
class TaskQueueAssignmentStatus(SimpleEnum):
    PENDING = "pending"
    RESERVED = "reserved"
    ASSIGNED = "assigned"
    COMPLETED = "completed"
