from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.teckst.element.mixin import TeckstMixin


@dataclass
class TeckstSendMessageComponent(BaseApiComponent, TeckstMixin):
    message: str = element_field(
        help="Text message to send to the phone number"
    )
