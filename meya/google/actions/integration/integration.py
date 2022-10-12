from dataclasses import dataclass
from meya.element.field import element_field
from meya.voice.integration.integration import VoiceIntegration
from typing import ClassVar


@dataclass
class GoogleActionsIntegration(VoiceIntegration):
    """
    # Google Actions Console Setup
    1. Open the [Actions Console](https://console.actions.google.com/)
    2. Select an existing project or create a new project. Follow the prompts
       when creating a new project.
    3. Get your project ID:
      - Click on the overflow menu on the top right of the project page. It's
         just to the left of your profile picture.
      - Click on **Project settings**
      - Note your Project ID
    4. Enable Actions CLI API for your Actions project.
      - Go to the [Actions API](https://console.developers.google.com/apis/library/actions.googleapis.com)
        settings page on **Google APIs**.
      - Make sure your project is selected in the project selector on the top
        left of the **Actions API** page.
      - Click **ENABLE**.
      - This will allow you to use the `gactions` CLI tool to create and manage
        you actions and webhooks.

    # Actions & Webhook Setup
    ## Download `gactions` v2.2.4 CLI Tool

    For Linux:
    ```shell script
    curl -o gactions https://dl.google.com/gactions/updates/bin/linux/amd64/gactions/gactions
    chmod a+x gactions
    sudo install gactions /usr/local/bin
    ```

    For Mac:
    ```shell script
    curl -o gactions https://dl.google.com/gactions/updates/bin/darwin/amd64/gactions/gactions
    chmod a+x gactions
    sudo install gactions /usr/local/bin
    ```

    **Important:** Do not download the latest v3+ version of `gactions` from the
    website.

    Run gactions and upgrade if necessary:
    ```shell script
    gactions
    ```

    Check the correct version is installed, you should see `Version = 2.2.4` (or higher):
    ```shell script
    gactions --version
    ```

    ## Webhook Setup

    ### 1. Add the Google Actions Integration
    The first thing you need to do is add the Google Actions integration to
    your app, you do this by creating a YAML file in your app that
    specifies the Google Actions integration element.

    Here is an example: save the following YAML to a file called
    `google_actions.yaml` in your app's `integration/` directory:

    ```yaml
    id: google-actions
    type: meya.google.actions.integration
    sandbox: true
    ```

    Properties:
    - **id**: this is optional, if you do not provide this then the id of the
      integration will be the dot path of the YAML file e.g.
      `integration.google_actions`.
    - **type**: the dot path of the integration element in the SDK.
    - **sandbox**: This specifies whether this integration is "sandbox" mode.
      Set this to `true` when developing and `false` when in production.


    ### 2. Get Your Webhook URL
    Next you need to run `meya webhooks` to get a list of webhooks for all the
    integrations you've added to your app. Search for Google Actions webhook
    and copy the webhook URL. You'll need to paste this URL in your Actions
    Package file in the next step.

    ### 3. Create an Actions Package File
    You will need to create an Actions Package JSON file that defines how
    the Google Assistant will trigger your actions and ultimately send a
    webhook.

    Find more info about the Actions Package format [here](https://developers.google.com/assistant/conversational/df-asdk/reference/action-package/rest/Shared.Types/ActionPackage)

    Here's and example Actions Package JSON file: save this following JSON
    to a file called `actions.json`:

    ```json
    {
        "actions": [
            {
                "description": "Start Intent",
                "name": "START",
                "fulfillment": {
                    "conversationName": "meya"
                },
                "intent": {
                    "name": "actions.intent.MAIN"
                }
            },
            {
                "description": "Say-to Intent",
                "name": "SAY_TO",
                "fulfillment": {
                    "conversationName": "meya"
                },
                "intent": {
                    "name": "meya.intent.TEXT",
                    "parameters": [
                        {
                            "name": "text",
                            "type": "SchemaOrg_Text"
                        }
                    ],
                    "trigger": {
                        "queryPatterns": [
                            "$SchemaOrg_Text:text"
                        ]
                    }
                }
            }
        ],
        "conversations": {
            "meya": {
                "name": "meya",
                "url": "YOUR_WEBHOOK_URL",
                "fulfillmentApiVersion": 2,
                "inDialogIntents": [
                    {
                        "name": "actions.intent.CANCEL"
                    },
                    {
                        "name": "actions.intent.NO_INPUT"
                    }
                ]
            }
        }
    }
    ```

    Using the webhook URL you copied in the previous step, paste it into
    your the `actions.json` file where it says `YOUR_WEBHOOK_URL`.

    ### 4. Upload the Actions Package
    Next you need to update your Actions project. Run the fullowing command
    replacing `ACTIONS_FILE.json` with the path to the Action Package you
    created in the previous step and replacing `PROJECT_ID` with the project id
    you got from the Actions Console on setup.

    ```shell script
    gactions update --action_package ACTIONS_FILE.json --project PROJECT_ID
    ```

    ## Invocation Setup
    1. Select your project in the Actions Console.
    2. Click on the **Develop** tab.
    3. Click on the **Invocation** menu item on the left.
    4. Specify a unique invocation in **Display name** form.
    5. Click Save

    ## Test Your Integration

    First make sure you've pushed your latest app changes to ensure the Google
    Actions integration is loaded.

    ```shell script
    meya push
    ```

    1. Select your project in the Actions Console.
    2. Click on the **Test** tab.
    3. Select your device, the default is **Smart Display**.
    4. Initiate the conversation with saying or using the **"Talk to ..."**
       suggestion.
    """

    NAME: ClassVar[str] = "google-actions"
    sandbox: bool = element_field(default=False)
