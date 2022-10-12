from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import element_field
from meya.zendesk.support.element.mixin.base import ZendeskBaseMixin
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.user import ZendeskSupportUserGet


@dataclass
class ZendeskSupportTicketRxComponent(Component, ZendeskBaseMixin):
    thread_id: str = element_field()
    ticket: ZendeskSupportTicketGet = element_field()
    current_user: ZendeskSupportUserGet = element_field()
