from dataclasses import dataclass
from meya.element.field import element_field
from meya.voice.integration.integration import VoiceIntegration
from typing import ClassVar


@dataclass
class AlexaIntegration(VoiceIntegration):
    """
    # Alexa Developer Console Setup
    1. Open the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
    2. Select an existing skill or create a new skill. For a new skill:
      a. Select **Custom** for your model.
      b. Select **Provision your own** for your skill's backend resources.
      c. Select **Hello World Skill**.
    3. Make sure you're on the **Build** tab.
    4. Select the **Invocation** menu item and specify a unique invocation in
       **Skill Invocation Name** form.
    5. Click **Save Model**.

    # Interaction Model & Webhook Setup

    ## Interaction Model
    First you need to setup your skill's Interaction Model to allow Alexa to
    send user utterances to the Meya webhook.

    Under the **Build** tab, select **Interaction Model** > **JSON Editor**.
    Then copy the following JSON object and paste it into the JSON editor
    (make sure the **invocationName** is set correctly):

    ```json
    {
        "interactionModel": {
            "languageModel": {
                "invocationName": "YOUR_INVOCATION",
                "intents": [
                    {
                        "name": "CatchAll",
                        "slots": [
                            {
                                "name": "any",
                                "type": "AMAZON.Person"
                            }
                        ],
                        "samples": [
                            "{any}"
                        ]
                    },
                    {
                        "name": "AMAZON.CancelIntent",
                        "samples": [
                            "cancel"
                        ]
                    },
                    {
                        "name": "AMAZON.HelpIntent",
                        "samples": [
                            "i need help",
                            "help me",
                            "help"
                        ]
                    },
                    {
                        "name": "AMAZON.StopIntent",
                        "samples": [
                            "stop"
                        ]
                    },
                    {
                        "name": "AMAZON.NavigateHomeIntent",
                        "samples": [
                            "reset",
                            "go home",
                            "restart"
                        ]
                    }
                ],
                "types": []
            }
        }
    }
    ```

    - Click the **Save Model** button.
    - Click **Build Model**. Alexa will start training the Interaction Model.

    ## Webhook Setup

    ### 1. Add the Alexa Integration
    The first thing you need to do is add the Alexa integration to your app,
    you do this by creating a YAML file in your app that specifies the Alexa
    integration element.

    Here is an example: save the following YAML to a file called `alexa.yaml`
    in your app's `integration/` directory:

    ```yaml
    type: meya.amazon.alexa.integration
    skill_id: (@ vault.alexa.skill_id )
    ```

    Properties:
    - **id**: this is optional, if you do not provide this then the id of the
      integration will be the dot path of the YAML file e.g.
      `integration.alexa`.
    - **skill_id**: this is the Skill ID that was assigned when you first
      created the skill. In this case we saved the Skill ID in the apps' vault.
      You can find the Skill ID under the **Build > Endpoint** section.

    Next you need to get the Skill ID and add it to the app's vault:
    1. Download you app's vault file: `meya vault download --file vault.secrets.yaml`
    2. Get the Skill ID from the Alexa Developer Console:
      a. Go to **Build > Endpoint**
      b. Select **AWS Lambda ARN**
      c. Copy the Skill ID
    3. Add the `alexa.skill_id` key to the `vault.secrets.yaml` file. Paste the
       Skill ID as the value of the `alexa.skill_id` key.
    4. Upload the app's vault file: `meya vault upload --file vault.secrets.yaml`
    5. Push your app: `meya push`

    ### 2. Get Your Webhook URL
    Next you need to run `meya webhooks` to get a list of webhooks for all the
    integrations you've added to your app. Search for Alexa webhook
    and copy the webhook URL.

    ### 3. Setup the Skill's Endpoint
    1. Go to the **Build** tab in the Alexa Developer Console.
    2. Go to the **Endpoint** section.
    3. Select the **HTTPS** option.
    4. Paste the webhook URL in the **Default Region** form.
    5. Select the **My development endpoint has a certificate from a trusted
       authority** option for the **Select SSL certificate type** drop down
       form.
    6. Click **Save Endpoints**.

    ## Test Your Integration

    First make sure you've pushed your latest app changes to ensure the Alexa
    integration is loaded.

    ```shell script
    meya push
    ```

    1. Select your skill in the Alexa Developer Console.
    2. Click on the **Test** tab.
    3. Make sure you enable testing by selecting **Develop** in the drop down.
    4. Initiate the conversation with saying or typing your invocation.
    """

    NAME: ClassVar[str] = "alexa"
    skill_id: str = element_field()
    catch_all_intent_name: str = element_field(default="CatchAll")
    unhandled_intent_text: str = element_field(
        default="Sorry I could not help with that. Please try again."
    )
