from dataclasses import dataclass
from meya import env
from meya.csp.integration import CspIntegration
from meya.db.view.thread import ThreadMode
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.front.integration.security import parse_front_request_client_token
from meya.util.enum import SimpleEnum
from numbers import Real
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type


class FrontIntegrationMode(SimpleEnum):
    TRACKING = "tracking"
    TICKETING = "ticketing"


class FrontUnlinkThreadStatus(SimpleEnum):
    # TODO when add status events add this types here as well
    TRASH = "trash"


@dataclass
class FrontIntegration(CspIntegration):
    """
    ## API token
    https://app.frontapp.com/settings/tools/api

    - Create a new Front token
    - Save as this integration's API token

    ## Bot teammate
    https://app.frontapp.com/settings/global/teammates/list

    - Find or create a teammate
    - This integration will use the teammate for all bot conversations
    - Save the email address as this integration's bot teammate email

    ## Channel
    https://app.frontapp.com/settings/home

    - Find or create an inbox
    - Add a new custom channel
      - Enter a descriptive name
    - Under "API endpoints", add an outgoing URL
      - Use this integration's webhook URL
    - Under "API endpoints", find "cha_xxx" in the incoming URL
      - Save as this integration's channel ID

    ## Webhook
    https://app.frontapp.com/settings/integrations/native/edit/webhooks/settings

    - Enable the webhook integration
    - Turn on send full event details

    ## Rule
    https://app.frontapp.com/settings/home

    - Add a new rule
      - Enter a descriptive name
      - Make sure rule is active
    - Add 8 "When..." triggers
      - Inbound message is received
      - Outbound message is sent (new conversation)
      - Outbound reply is sent (existing conversation)
      - New comment is added from any teammate (no body condition)
      - Assignee is changed to any teammate
      - Assignee is removed
      - Any tag is added
      - Any tag is removed
    - [Optional] Add "If..." condition
      - Conversation is in your desired Inbox
    - Add 1 "Then..." action
      - "Send to a Webhook": Paste this integration's webhook URL

    ## Meya Partner Channel
    To use the Meya Partner Channel you'll need to generate a new token for
    Front, and set it as the Front integration `client_token`.

    - Create a new client token using your app ID, integration ID, and a client
      secret that you generate using a password generator
      - Token format: {{app_id}}:{{integration_id}}:{{client_secret}},
        e.g. app-123:integration.front:xyz789
      - `client_secret` must be alphanumeric with length 10 to 20 characters
    - Now go to your Front inbox settings, and add the `Meya Partner Channel`
      using this client token
    """

    NAME: ClassVar[str] = "front"

    api_token: str = element_field()
    bot_teammate_email: str = element_field()
    channel_id: str = element_field()
    integration_mode: FrontIntegrationMode = element_field(
        default=FrontIntegrationMode.TRACKING
    )
    unlink_thread_status: Optional[
        List[FrontUnlinkThreadStatus]
    ] = element_field(
        default_factory=list,
        help=(
            "The set of Front statuses that will unlink the "
            "Meya thread from the Front conversation. "
            "When the Meya thread is unlinked, then the integration will "
            "no longer send events to Front."
        ),
    )
    unassign_mode: Optional[str] = element_field(default=ThreadMode.BOT)
    client_token: Optional[str] = element_field(default=None)
    request_attempts: Optional[int] = element_field(
        default=4,
        help=(
            "Controls the number of attempts of each API request on the "
            "conversation create component."
        ),
    )
    request_timeout: Optional[Real] = element_field(
        default=3, help="Controls Front API request timeout."
    )
    max_attachment_size: Optional[int] = element_field(
        default=15 * 1024 * 1024,
        help=(
            "Controls maximum attachment size supported by the integration in "
            "bytes."
        ),
    )

    def validate(self):
        super().validate()
        if self.client_token:
            app_id, integration_id = parse_front_request_client_token(
                self.client_token
            )
            if app_id != env.app_id:
                raise self.validation_error(
                    f"Invalid client token, expected app ID to be '{env.app_id}'"
                )
            if integration_id != self.id:
                raise self.validation_error(
                    f"Invalid client token, expected integration ID to be '{self.id}'"
                )
        if (
            self.integration_mode == FrontIntegrationMode.TRACKING
            and self.unlink_thread_status
        ):
            raise self.validation_error(
                f"Tracking mode doesn't support the use of "
                f"`unlink_thread_status` since the thread is always linked "
                f"on tracking mode."
            )


class FrontIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = FrontIntegration
