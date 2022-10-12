from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.teckst.element.mixin import TeckstMixin
from typing import Optional


@dataclass
class TeckstSendMediaComponent(BaseApiComponent, TeckstMixin):
    media_url: str = element_field(
        help="Media file URL to send to the phone number"
    )
    message: Optional[str] = element_field(
        default=None, help="Text message to send to the phone number"
    )
