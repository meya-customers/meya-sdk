from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.widget.event import WidgetEvent
from typing import Any
from typing import Optional


@dataclass
class FieldEvent(WidgetEvent):
    field_id: Optional[str] = entry_field(default_missing=True, default=None)
    submit_button_id: Optional[str] = entry_field(
        default_missing=True, default=None
    )
    required: bool = entry_field(default_missing=True, default=False)
    label: Optional[str] = entry_field(
        default_missing=True, default=None, sensitive=True
    )
    disabled: bool = entry_field(default_missing=True, default=False)
    ok: Optional[bool] = entry_field(default_missing=True, default=None)
    error: Optional[str] = entry_field(
        default_missing=True, default=None, sensitive=True
    )
    input_data: Any = entry_field(
        default_missing=True, default=None, sensitive=True
    )
