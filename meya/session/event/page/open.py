from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.lifecycle.event.event import LifecycleEvent
from typing import Optional


@dataclass
class PageOpenEvent(LifecycleEvent):
    lifecycle_id: str = entry_field(default="page_open")
    text: Optional[str] = entry_field(default=None)
    url: str = entry_field()
    magic_link_ok: Optional[bool] = entry_field(default=None)
    referrer: Optional[str] = entry_field(default=None)
    user_agent: Optional[str] = entry_field(default=None)
    ip_address: Optional[str] = entry_field(default=None)
    accept_language: Optional[str] = entry_field(default=None)
