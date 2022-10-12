from abc import ABC
from dataclasses import dataclass
from meya.util.context_var import ScopedContextVar
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Set
from typing import cast


@dataclass
class AbstractTypeRegistry(ABC):
    items: List[type]
    alias: Dict[str, type]
    reverse_alias: Dict[type, str]
    private: Dict[type, type]
    subclasses: Dict[type, Set[type]]

    current: ClassVar = cast(
        ScopedContextVar["AbstractTypeRegistry"], ScopedContextVar()
    )
