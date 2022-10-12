from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.conversation import FrontConversationMixin
from meya.front.integration import FrontIntegration
from meya.front.integration import FrontIntegrationMode
from meya.front.payload.contact import FrontSource
from meya.front.payload.conversation import FrontCreateConversationResponse
from meya.util.dict import MISSING_FACTORY
from typing import List
from typing import Optional


@dataclass
class FrontConversationCreateComponentResponse:
    result: FrontCreateConversationResponse = response_field(sensitive=True)


@dataclass
class FrontConversationCreateComponent(
    BaseApiComponent, FrontConversationMixin
):
    thread_ref: Optional[str] = element_field(
        default=None,
        help=(
            "A way of uniquely identifying the Meya thread the conversation "
            "is associated with. Defaults to meya_thread/<Meya thread ID>"
        ),
    )
    contact_handle: Optional[str] = element_field(
        default=None,
        help=(
            "An alias for the Front Contact. The format is "
            "alt:<source>:<handle> (e.g. alt:phone:+12345678900). Defaults "
            "to meya_user/<Meya user ID>"
        ),
    )
    contact_source: Optional[FrontSource] = element_field(
        default=FrontSource.CUSTOM,
        help=(
            "Front contact source. e.g. `email`. "
            "Front enforces contact handle format depending on the contact "
            "source, e.g., for twitter the contact handle must start with `@`."
            "This value will only be used in case of contact creation."
        ),
    )
    contact_id: Optional[str] = element_field(
        default=None, help="Front Contact ID"
    )
    subject: Optional[str] = element_field(
        default=None, help="The subject of the message"
    )

    send_transcript: bool = element_field(
        default=True,
        help=(
            "Whether or not the chat transcript should be included in the "
            "conversation. Useful for providing context for agents"
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

    link: bool = element_field(
        default=True,
        help="Link the current Meya thread to this integration thread",
    )

    def validate(self):
        integration: FrontIntegration = self.from_spec(  # noqa
            self.resolve_spec(self.integration)
        )
        if (
            integration.integration_mode.value
            == FrontIntegrationMode.TRACKING.value
            and not self.thread_ref
        ):
            raise self.validation_error(
                "You need to add a thread ref id when using this component with tracking mode"
            )

        if not self.text and not self.html and not self.send_transcript:
            raise self.validation_error(
                "You need to either send a text or html or choose to send transcript in order to create a conversation"
            )
