from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.element.mixin.ticket import ZendeskTicketMixin
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from typing import Optional


@dataclass
class ZendeskSupportTicketCreateComponent(
    BaseApiComponent, ZendeskTicketMixin
):
    """
    Create a new Zendesk Support ticket.

    Here is an example of a simple ticket creation flow that first asks the
    user for their name, email, and phone number, and then creates a ticket:

    ```yaml
    triggers:
      - keyword: zendesk_support_ticket_create
        when: true
    steps:
      - ask: Link user?
        buttons:
          - text: Yes
            result: true
          - text: No
            result: false
      - flow_set: link_user
      - if: (@ flow.link_user )
        then:
          jump: link_ticket
        else:
          next:
      - flow_set:
          link_ticket: false
      - jump: name

      - (link_ticket)
      - ask: Link ticket?
        buttons:
          - text: Yes
            result: true
          - text: No
            result: false
      - flow_set: link_ticket

      - (name)

      # Start "prechat" mode to collect sensitive details, all user responses will be encrypted
      - mode: prechat

      - say: Name?
      - type: text_input
        required: true
        label: Name
        icon: (@ config.icon.person )
        quick_replies:
          - text: Skip (generate)
            result:
      - flow_set: name

      - say: Email?
      - type: email_address_input
        required: true
        quick_replies:
          - text: Skip (blank)
            result:
      - flow_set: email

      - say: Phone?
      - type: text_input
        required: true
        label: Phone
        icon: (@ config.icon.phone )
        quick_replies:
          - text: Skip (blank)
            result:
      - flow_set: phone

      - say: Subject?
      - type: text_input
        required: true
        label: Ticket subject
        quick_replies:
          - text: Skip (generate)
            result:
      - flow_set: subject

      - say: Comment?
      - type: text_input
        required: true
        label: Ticket comment
        quick_replies:
          - text: Skip (use transcript)
            result:
      - flow_set: comment

      # Done "prechat" mode
      - mode:

      - (create)
      - note: This is a note before ticket creation
      - say: Creating or updating user...
      - type: meya.zendesk.support.component.user.create_or_update
        integration: integration.zendesk.support
        link: (@ flow.link_user )
        name: (@ flow.name )
        email: (@ flow.email )
        phone: (@ flow.phone )
      - say: User (@ flow.result.id ) created or updated
      - say: Creating ticket...
      - type: meya.zendesk.support.component.ticket.create
        integration: integration.zendesk.support
        link: (@ flow.link_ticket )
        requester_id: (@ flow.result.id )
        subject: (@ flow.subject )
        comment: (@ flow.comment )
        ticket_form_id: (@ vault.zendesk.support.ticket_form_id )
        brand_id: (@ vault.zendesk.support.brand_id )
      - say: Ticket (@ flow.result.id ) created
      - note: This is a note after ticket creation
      - end
    ```
    """

    @dataclass
    class Response:
        result: ZendeskSupportTicketGet = response_field(sensitive=True)

    link: bool = element_field(
        default=True,
        help=(
            "Whether to link the ticket to the current Meya thread. This "
            "will use the Zendesk ticket ID returned from the API response as "
            "the integration thread ID for Meya to link to. If the "
            "`external_id` is not set explicitly in this component, then the "
            "Meya thread ID will be used as the external ID on the Zendesk "
            "ticket for reference."
        ),
    )
    followup: bool = element_field(
        default=True,
        help=(
            "Whether this new ticket is a followup to an existing ticket that "
            "was previously created and linked to the current Meya thread. "
            "If the previous ticket ID can be resolved from the current Meya "
            "thread, then the old ticket will be marked as `Closed` and it's "
            "ticket ID will be used as the `via_followup_source_id` on the "
            "new ticket."
        ),
    )
    via_followup_source_id: Optional[int] = element_field(
        default=None,
        help=(
            "The ID of the ticket that this new ticket is a followup to. "
            "Note, this value will be overridden if the `followup` field is "
            "set to `True` and a previous ticket ID can be resolved from the "
            "current Meya thread."
        ),
    )
