from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.conversation import FrontConversationMixin
from meya.front.payload.message import FrontSendIncomingMessageResponse
from typing import Optional


@dataclass
class FrontMessageSendComponentResponse:
    result: FrontSendIncomingMessageResponse = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontMessageSendComponent(BaseApiComponent, FrontConversationMixin):
    thread_ref: Optional[str] = element_field(
        default=None,
        help=(
            "A way of uniquely identifying the Meya thread the conversation "
            "is associated with. Defaults to meya_thread/<Meya thread ID>"
        ),
    )
    conversation_id: Optional[str] = element_field(
        default=None,
        help=(
            "The Front conversation ID. "
            "Conversation IDs have the format cnv_xxxxxxxx"
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
    contact_id: Optional[str] = element_field(
        default=None, help="The Front Contact ID"
    )

    subject: Optional[str] = element_field(
        default=None, help="The subject of the message"
    )

    send_transcript: bool = element_field(
        default=False,
        help=(
            "Send the chat transcript to be included in the "
            "conversation. Useful for providing context for agents."
        ),
    )

    def validate(self):
        if (
            self.text or self.html or self.attachments_url
        ) and self.send_transcript:
            raise self.validation_error(
                "You can't send text or HTML or attachments together with the "
                "conversation transcript. Make sure to use this component "
                "twice instead. "
                "This is necessary to ensure Front consistency."
            )
        if (
            not self.text
            and not self.html
            and not self.attachments_url
            and not self.send_transcript
        ):
            raise self.validation_error(
                "You need to send text, html, attachment or "
                "the conversation transcript"
            )
