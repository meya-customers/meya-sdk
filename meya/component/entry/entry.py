from dataclasses import dataclass
from meya.bot.entry import BotEntry
from meya.entry.field import entry_field
from meya.flow.stack_frame import StackFrame
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class ComponentEntry(BotEntry):
    data: Dict[str, Any] = entry_field()
    flow: Optional[str] = entry_field()
    index: Optional[int] = entry_field()
    spec: Dict[str, Any] = entry_field()
    stack: Optional[List[StackFrame]] = entry_field()
