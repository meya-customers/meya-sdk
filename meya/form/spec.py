from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.util.dict import MISSING_FACTORY
from typing import Any
from typing import Union


@dataclass
class SelectOptionCommonSpec:
    text: str = entry_field(help="Text shown for this option")
    disabled: bool = entry_field(
        default=False, help="Whether the option is disabled / un-selectable"
    )


@dataclass
class SelectOptionEventSpec(SelectOptionCommonSpec):
    pass


@dataclass
class SelectOptionElementSpec(SelectOptionCommonSpec):
    value: Any = entry_field(
        default_factory=MISSING_FACTORY,
        help="Value override for this option (not shown)",
    )


SelectOptionElementSpecUnion = Union[SelectOptionElementSpec, str]
