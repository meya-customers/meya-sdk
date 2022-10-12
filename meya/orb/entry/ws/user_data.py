from dataclasses import dataclass
from meya.db.view.user import UserType
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class OrbUserData:
    name: Optional[str]
    avatar: Optional[Dict[str, Any]]
    type: UserType
