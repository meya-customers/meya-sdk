from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import element_field
from meya.zendesk.support.element.mixin.base import ZendeskBaseMixin
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.user import ZendeskSupportUserGet


@dataclass
class ZendeskSupportTicketRxComponent(Component, ZendeskBaseMixin):
    """
    This component will run the Zendesk Support integration's internal
    `ticket_rx` logic and publish any relevant events to the Meya thread.

    This component is mainly used when implementing agent-initiated
    conversations with Zendesk Support. Check the
    [agent-initiated conversations guide](https://docs.meya.ai/docs/sending-agent-initiated-conversations-with-zendesk-support-and-zendesk-sunshine-conversations)
    for more information.
    """

    thread_id: str = element_field(
        help="The ID of the Meya relevant thread.",
    )
    ticket: ZendeskSupportTicketGet = element_field(
        help="The ticket API response payload from the Zendesk API."
    )
    current_user: ZendeskSupportUserGet = element_field(
        help="The user API response payload from the Zendesk API."
    )
