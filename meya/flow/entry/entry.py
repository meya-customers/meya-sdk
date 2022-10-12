from dataclasses import dataclass
from meya.bot.entry import BotEntry
from meya.entry.field import entry_field
from meya.flow.stack_frame import StackFrame
from typing import Any
from typing import Dict
from typing import List


@dataclass
class FlowEntry(BotEntry):
    data: Dict[str, Any] = entry_field()
    flow: str = entry_field()
    stack: List[StackFrame] = entry_field()
