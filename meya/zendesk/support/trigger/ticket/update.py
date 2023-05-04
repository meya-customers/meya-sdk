from dataclasses import dataclass
from meya.element.field import process_field
from meya.element.field import response_field
from meya.http.trigger import WebhookTrigger
from meya.zendesk.support.event.ticket.update import (
    ZendeskSupportTicketUpdateEvent,
)
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet


@dataclass
class ZendeskSupportTicketUpdateTrigger(WebhookTrigger):
    """
    This trigger will match any incoming Zendesk Support ticket update
    webhooks and will return the old version of the ticket and the new
    version of the ticket.

    This trigger is particularly useful if you would like to display ticket
    status changes to the users. Here is an example of how you can use this:

    ```yaml
    triggers:
      - type: meya.zendesk.support.trigger.ticket.update
        bot: bot.notification

    steps:
      - (check_status)
      - if: (@ flow.ticket.status != flow.old_ticket.status )
        then: next
        else:
          jump: check_assignee
      - status: Ticket (@ flow.ticket.id) is now (@ flow.ticket.status )

      - (check_assignee)
      - if: (@ flow.ticket.assignee_id != flow.old_ticket.assignee_id )
        then: next
        else:
          jump: solved
      - if: (@ not flow.ticket.assignee_id )
        then:
          jump: no_assignee
        else: next
      - type: meya.zendesk.support.component.user.show
        integration: integration.zendesk.support
        user_id: (@ flow.ticket.assignee_id )
      - status: >
          Ticket (@ flow.ticket.id) is now assigned to
          (@ flow.result.alias or flow.result.name )
      - jump: solved

      - (no_assignee)
      - status: Ticket (@ flow.ticket.id) status is now unassigned
      - jump: solved

      - (solved)
      - if: (@ flow.ticket.status != flow.old_ticket.status and flow.ticket.status ==
          "solved" )
        then:
          flow: flow.zendesk.support.webhook.ticket_solved
          bot: bot.default
          async: true
        else: end
    ```

    This flow will check if the ticket status has changed and if it has, it will
    display the new status to the user. It will also check if the ticket has
    been assigned to a new agent and if it has, it will display the new agent
    to the user. Finally, if the ticket has been solved, it will run a
    nested flow called `flow.zendesk.support.webhook.ticket_solved`.

    One thing to note is that this flow runs as a separate bot called
    `bot.notification`. This is because the `bot.default` bot is used for
    the main flow, and we don't want incoming Zendesk Support webhooks to
    change the user's main flow.
    """

    entry: ZendeskSupportTicketUpdateEvent = process_field()
    encrypted_entry: ZendeskSupportTicketUpdateEvent = process_field()

    @dataclass
    class Response:
        ticket: ZendeskSupportTicketGet = response_field(sensitive=True)
        old_ticket: ZendeskSupportTicketGet = response_field(sensitive=True)
