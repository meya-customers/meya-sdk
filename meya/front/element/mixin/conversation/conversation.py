from dataclasses import dataclass
from meya.element.field import element_field
from meya.front.element.mixin.base import FrontMixin
from meya.util.dict import MISSING_FACTORY
from typing import List
from typing import Optional


@dataclass
class FrontConversationMixin(FrontMixin):
    attachments_url: List[str] = element_field(
        default_factory=list,
        help="A list of file URLs to attach to the conversation",
    )
    text: Optional[str] = element_field(
        default=None, help="The plain text version of the message"
    )
    html: Optional[str] = element_field(
        default=None, help="The HTML version of the message"
    )
