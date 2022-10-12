from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.user.entry import UserEntry
from typing import Any


@dataclass
class UserDataEntry(UserEntry):
    key: str = entry_field()
    value: Any = entry_field()
