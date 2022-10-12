from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.user.entry import UserEntry


@dataclass
class UserLinkEntry(UserEntry):
    integration_id: str = entry_field()
    integration_user_id: str = entry_field()
