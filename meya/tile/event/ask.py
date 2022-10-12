from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from meya.tile.spec import TileButtonStyle
from meya.tile.spec import TileEventSpec
from meya.tile.spec import TileLayout
from typing import List
from typing import Optional


@dataclass
class TileAskEvent(InteractiveEvent):
    button_style: Optional[TileButtonStyle] = entry_field()
    layout: Optional[TileLayout] = entry_field()
    text: Optional[str] = entry_field(default=None, sensitive=True)
    tiles: List[TileEventSpec] = entry_field(sensitive_factory=list)
