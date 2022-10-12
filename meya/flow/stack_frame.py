from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass
class StackFrame:
    data: Dict[str, Any]
    flow: str
    index: int
