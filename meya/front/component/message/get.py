from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.message import FrontMessageDetails


@dataclass
class FrontMessageGetComponentResponse:
    result: FrontMessageDetails = response_field(sensitive=True, default=None)
    conversation_id: str = response_field(sensitive=True, default=None)
    ok: bool = response_field(default=True)


@dataclass
class FrontMessageGetComponent(BaseApiComponent, FrontMixin):
    message_uid: str = element_field()
    alias_prefix: str = element_field(default="alt:uid")
