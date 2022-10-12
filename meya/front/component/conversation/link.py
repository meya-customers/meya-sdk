from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin


@dataclass
class FrontConversationLinkComponentResponse:
    ok: bool = response_field(default=True)


@dataclass
class FrontConversationLinkComponent(BaseApiComponent, FrontMixin):
    message_uid: str = element_field(default=None)
