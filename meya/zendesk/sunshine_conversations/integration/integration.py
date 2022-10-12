from dataclasses import dataclass
from enum import Enum
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element.interactive import InteractiveIntegration
from typing import ClassVar
from typing import Type


class SunshineConversationsRegion(Enum):
    US = "us"
    EU = "eu"


@dataclass
class SunshineConversationsIntegration(InteractiveIntegration):
    """
    # Webhook Setup

    ## 1. Add the Sunshine Conversations Integration
    The first thing you need to do is add the Sunshine Conversations integration
    to your app, you do this by creatign a YAML file in you app that specifies
    the Sunshine Conversations integration element.

    Here is an example: save the following YAML to a file called
    `sunshine_conversations.yaml` in your app's `integration/` directory.

    ```yaml
    id: sunshine-conversations
    type: meya.zendesk.sunshine_conversations.integration
    key_id: (@ vault.sunshine_conversations.api_key_id )
    secret: (@ vault.sunshine_conversations.api_secret )
    ```

    Properties:
    - **id**: this is optional, if you do not provide this then the id of the
      integration will be the dot path of the YAML file e.g.
      `integration.sunshine_conversations`.
    - **type**: the dot path of the integration element in the SDK.
    - **key_id**: this is your Sunshine Conversation app's API key ID.
    - **secret**: this is your Sunshine Conversation app's API secret.

    Next you need to get your Sunshine Conversation app's API **key_id** and
    **secret**:
    1. Download your app's vault file: `meya vault download --file vault.secrets.yaml`
    2. Go the the [Sunshine Conversations Console](https://app.smooch.io/)
    3. Select an existing app or create a new app.
    4. Go to the **Settings** tab.
    5. Scroll to the **API Keys** section.
    6. Select or create a new API Key.
    7. Copy the ID of the API key and add it to your vault file under the
       `sunshine_conversations.api_key_id` key.
    8. Copy the SECRET of API key and add it to your vault file under the
       `sunshine_conversations.api_secret` key.
    9. Upload your app's vault file: `meya vault upload --file vault.secrets.yaml`
    10. Push your app: `meya push`

    ## 2. Get Your Webhook URL
    Next you need to run `meya webhooks` to get a list of webhooks for all the
    integrations you've added to your app. Search for Sunshine Conversations webhook
    and copy the webhook URL.

    ## 3. Add a Webhook to Your Sunshine Conversations App
    1. Go the the [Sunshine Conversations Console](https://app.smooch.io/)
    2. Go to the **Integrations** tab.
    3. Search for the **Webhooks** integrations.
    4. In the Webhooks integration page, click on **Connect** for a new integration,
       or **Configure** for and existing webhook.
    5. Click on **Create a webhook**.
    6. Paste the webhook URL you copied earlier into the **Webhook URL** form.
    7. Select **v1.1** in the **Version** drop down.
    8. Check:
      - All basic triggers
      - User typing
    9. Click **Create webhook**

    You should now be able to add other integration e.g. Web Messenger, Telegram,
    Slack etc.
    """

    NAME: ClassVar[str] = "sunshine-conversations"

    app_id: str = element_field()
    key_id: str = element_field()
    secret: str = element_field()
    region: SunshineConversationsRegion = element_field(
        default=SunshineConversationsRegion.US
    )
    lifecycle_events: bool = element_field(default=True)


class SunshineConversationsIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = SunshineConversationsIntegration
