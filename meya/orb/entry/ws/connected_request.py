from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.orb.entry.ws.request import OrbWsRequestEntry
from meya.orb.entry.ws.user_data import OrbUserData
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class OrbWsConnectedRequestEntry(OrbWsRequestEntry):
    grid_version: str = entry_field()
    config: Dict[str, Dict[str, Any]] = entry_field(default_factory=dict)
    history_events: List[Dict[str, Any]] = entry_field(default_factory=list)
    history_user_data: Dict[str, OrbUserData] = entry_field(
        default_factory=dict
    )
    user_id: str = entry_field()
    session_token: str = entry_field()
    grid_user_id: str = entry_field()
    grid_thread_id: str = entry_field()
    magic_link_ok: Optional[bool] = entry_field(default=None)
    magic_link_event: Optional[Dict[str, Any]] = entry_field(default=None)
    heartbeat_interval_seconds: Optional[int] = entry_field(default=None)
