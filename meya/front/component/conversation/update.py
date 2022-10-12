from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.conversation import FrontConversationMixin
from meya.util.dict import MISSING_FACTORY
from typing import List
from typing import Optional


@dataclass
class FrontConversationUpdateComponentResponse:
    ok: bool = response_field(default=True)


@dataclass
class FrontConversationUpdateComponent(
    BaseApiComponent, FrontConversationMixin
):
    conversation_id: Optional[str] = element_field(
        default=None,
        help=(
            "The Front conversation ID. "
            "Conversation IDs have the format cnv_xxxxxxxx"
        ),
    )
    assignee_id: Optional[str] = element_field(
        default_factory=MISSING_FACTORY,
        help=(
            "The Front ID of the teammate to assign the conversation to. "
            "Set it to null to unassign. Teammate IDs have the format tea_xxxx"
        ),
    )
    assignee_email: Optional[str] = element_field(
        default_factory=MISSING_FACTORY,
        help=(
            "The email of the teammate to assign the conversation to. "
            "Set it to null to unassign."
        ),
    )
    inbox_id: Optional[str] = element_field(
        default=None,
        help=(
            "The Front ID of the inbox to move the conversation to. "
            "Inbox IDs have the format inb_xxxxx"
        ),
    )
    status: Optional[str] = element_field(
        default=None, help="The new status of the conversation"
    )
    tag_ids: Optional[List[str]] = element_field(
        default=None,
        help="A list of Front tag IDs. Tag IDs have the format tag_xxxxxx",
    )
