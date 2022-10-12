from meya.teckst.payload import TeckstMedia
from meya.teckst.payload import TeckstMediaWebhook
from meya.teckst.payload import TeckstSendMessagePayload
from meya.teckst.payload import TeckstWebhook


def test_teckst_payload():
    assert TeckstSendMessagePayload.from_dict(
        {
            "crm": "crm",
            "crmChannelIdentifier": "crm channel",
            "contactChannelIdentifier": "contact channel identifier",
            "status": "status",
            "body": "body",
            "media": [
                {
                    "url": "https://media.giphy.com/media/WWyT3VgEgIK8U/giphy.gif"
                }
            ],
        }
    ) == TeckstSendMessagePayload(
        crm="crm",
        crm_channel_identifier="crm channel",
        contact_channel_identifier="contact channel identifier",
        status="status",
        body="body",
        media=[
            TeckstMedia(
                url="https://media.giphy.com/media/WWyT3VgEgIK8U/giphy.gif"
            )
        ],
    )


def test_teckst_webhook():
    assert TeckstWebhook.from_dict(
        {
            "media": [],
            "content": "Hi",
            "crmChannelIdentifier": "+16154888477",
            "contactChannelIdentifier": "+12268084934",
        }
    ) == TeckstWebhook(
        media=[],
        content="Hi",
        crm_channel_identifier="+16154888477",
        contact_channel_identifier="+12268084934",
    )


def test_teckst_media_webhook():
    assert TeckstWebhook.from_dict(
        {
            "media": [
                {
                    "url": "https://s3.amazonaws.com/teckst_attachments_production/d98c6a42-52bf-46cd-9681-007ea2b44112",
                    "longUrl": "https://s3.amazonaws.com/teckst_attachments_production/d98c6a42-52bf-46cd-9681-007ea2b44112",
                }
            ],
            "content": " https://s3.amazonaws.com/teckst_attachments_production/d98c6a42-52bf-46cd-9681-007ea2b44112",
            "crmChannelIdentifier": "+16154888477",
            "contactChannelIdentifier": "+12268390208",
        }
    ) == TeckstWebhook(
        media=[
            TeckstMediaWebhook(
                url="https://s3.amazonaws.com/teckst_attachments_production/d98c6a42-52bf-46cd-9681-007ea2b44112",
                long_url="https://s3.amazonaws.com/teckst_attachments_production/d98c6a42-52bf-46cd-9681-007ea2b44112",
            )
        ],
        content=" https://s3.amazonaws.com/teckst_attachments_production/d98c6a42-52bf-46cd-9681-007ea2b44112",
        crm_channel_identifier="+16154888477",
        contact_channel_identifier="+12268390208",
    )
