from dataclasses import dataclass
from meya.csp.integration import CspIntegration
from meya.element import Element
from meya.element.field import element_field
from meya.twilio.integration.base import TwilioBaseIntegration
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from typing import ClassVar
from typing import Type


@dataclass
class TwilioFlexIntegration(CspIntegration, TwilioBaseIntegration):
    """
    ## Meya app setup
    - Add Twilio Flex integration to your Meya app
    - Get integration webhook and save for later
    `meya webhooks | grep twilio_flex`

    ## Twilio Flex setup

    ### Create API Key
    - Access API Key management
    `https://www.twilio.com/console/project/api-keys`
    - Create a new API Key
    - Add the new SID and secret to
    `(@ vault.twilio.api_key_sid )` and `(@ vault.twilio.api_key_secret )`
    respectively

    ### Enable Flex
    - Access your Twilio account
    `https://www.twilio.com/console`
    - Add account SID to `(@ vault.twilio_flex.account_sid )`
    - Enable Twilio Flex
    `https://www.twilio.com/console/flex/overview`

    ### Enable Programmable Chat webhooks
    - Access [Flex Channel Service](https://www.twilio.com/console/chat/dashboard) created by Flex setup
    - Add service SID to `(@ vault.twilio_flex.flex_chat_service )`
    - Go to webhooks on side menu and add Meya webhook saved earlier to "Post-Event Webhooks"
    - Enable `onMessageSent` and `onMediaMessageSent`

    ### Enable Task Router webhooks
    - Access your [Task Router Workspace](https://www.twilio.com/console/taskrouter/workspaces)
    - Go to settings on side menu and add Meya webhook to `Event Callbacks`
    - Enable `Reservation Accepted`, `Reservation Completed`, `Task Canceled` and `TaskQueueEntered` events

    ### Setup Web channel
    - Access [Flex Messaging Settings](https://www.twilio.com/console/flex/messaging)
    - Edit `web` channel
    - Set `INTEGRATION TYPE` to `Task`
    - Set `TASK CHANNEL` to `Programmable Chat`

    ### Launch Twilio Flex
    - Access your [Flex Instance](https://www.twilio.com/console/flex/overview)
    - Inside Flex instance go to Admin > Developer setup
    - Add `flexFlowSid` to `(@ vault.twilio_flex.flex_flow_sid )`
    """

    NAME: ClassVar[str] = "twilio_flex"
    flex_flow_sid: str = element_field(meta_name="Twilio Flex flow SID")
    flex_chat_service_sid: str = element_field(
        meta_name="Twilio Flex chat service SID"
    )


class TwilioFlexIntegrationRef(TwilioBaseIntegrationRef):
    element_type: ClassVar[Type[Element]] = TwilioFlexIntegration
