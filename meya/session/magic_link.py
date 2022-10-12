from dataclasses import dataclass
from dataclasses import field
from numbers import Real
from time import time
from typing import Optional


@dataclass
class MagicLink:
    integration_id: str
    expires: Real
    single_use: bool
    event: Optional[dict]
    is_expired: bool = field(init=False)

    def __post_init__(self):
        self.is_expired = float(self.expires) < time()
