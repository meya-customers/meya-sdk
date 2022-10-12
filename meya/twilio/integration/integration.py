from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.integration.element.interactive import InteractiveIntegration
from meya.twilio.integration.base import TwilioBaseIntegration
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from meya.twilio.payload.webhook import TwilioMessageStatus
from typing import ClassVar
from typing import List
from typing import Type


@dataclass
class TwilioIntegration(InteractiveIntegration, TwilioBaseIntegration):
    """
    ## Twilio setup

    ### Create API Key
    - Access API Key management
    `https://www.twilio.com/console/project/api-keys`
    - Create a new API Key
    - Add the new SID and secret to
    `(@ vault.twilio.api_key_sid )` and `(@ vault.twilio.api_key_secret )`
    respectively

    ### Account SID
    - Access your Twilio account
    `https://www.twilio.com/console`
    - Add account SID to `(@ vault.twilio.account_sid )`

    ### Phone number
    - Access `Phone Numbers` under `SUPER NETWORK` menu
    - Add the active phone number to `(@ vault.twilio.phone_number )`
    """

    NAME: ClassVar[str] = "twilio"
    extra_sms_status_events: List[TwilioMessageStatus] = element_field(
        default_factory=list,
        meta_name="extra SMS status events",
        help=(
            "List of SMS events that you want to process. "
            "This is useful in case you need specific behaviours depending on "
            "the status of the message. "
            "For WhatsApp Integration the `TwilioSmsSentEvent` is changed to "
            "`WhatsAppSentEvent` for standard messages and "
            "`WhatsAppSentTemplateEvent` for template messages. "
            "For more information on WhatsApp template access: "
            "https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates"
        ),
    )


class TwilioIntegrationRef(TwilioBaseIntegrationRef):
    element_type: ClassVar[Type[Element]] = TwilioIntegration
