from dataclasses import dataclass
from meya.thread.event import ThreadEvent


@dataclass
class ThreadStartEvent(ThreadEvent):
    pass
