import pytest

from meya.twilio.payload.webhook import TwilioMessageStatus
from meya.twilio.payload.webhook import TwilioWebhook


@pytest.mark.parametrize(
    ("payload_dict", "twilio_webhook"),
    [
        (
            {
                "To": "+12267795840",
                "From": "+12268390208",
                "SmsSid": "MM01bee17087bd6a4e22c76bf9776f2fc6",
                "ToCity": "STRATFORD",
                "ToState": "ON",
                "NumMedia": "1",
                "FromState": "Ontario",
                "MediaUrl0": "https://api.twilio.com/2010-04-01/Accounts/AC736c024b7f0763e7e0268af61611f0d7/Messages/MM01bee17087bd6a4e22c76bf9776f2fc6/Media/ME0636d28e5bb77b2d70b8ab9f9d093cc5",
                "SmsStatus": "received",
                "ToCountry": "CA",
                "AccountSid": "AC736c024b7f0763e7e0268af61611f0d7",
                "ApiVersion": "2010-04-01",
                "MessageSid": "MM01bee17087bd6a4e22c76bf9776f2fc6",
                "FromCountry": "CA",
                "NumSegments": "1",
                "SmsMessageSid": "MM01bee17087bd6a4e22c76bf9776f2fc6",
                "MediaContentType0": "image/jpeg",
            },
            TwilioWebhook(
                To="+12267795840",
                From="+12268390208",
                SmsSid="MM01bee17087bd6a4e22c76bf9776f2fc6",
                ToCity="STRATFORD",
                ToState="ON",
                NumMedia="1",
                FromState="Ontario",
                MediaUrl0="https://api.twilio.com/2010-04-01/Accounts/AC736c024b7f0763e7e0268af61611f0d7/Messages/MM01bee17087bd6a4e22c76bf9776f2fc6/Media/ME0636d28e5bb77b2d70b8ab9f9d093cc5",
                SmsStatus=TwilioMessageStatus.RECEIVED,
                ToCountry="CA",
                AccountSid="AC736c024b7f0763e7e0268af61611f0d7",
                ApiVersion="2010-04-01",
                MessageSid="MM01bee17087bd6a4e22c76bf9776f2fc6",
                FromCountry="CA",
                NumSegments="1",
                SmsMessageSid="MM01bee17087bd6a4e22c76bf9776f2fc6",
                MediaContentType0="image/jpeg",
            ),
        ),
        (
            {
                "To": "whatsapp:+14155238886",
                "From": "whatsapp:+554799930448",
                "WaId": "554799930448",
                "SmsSid": "MM4c01e4547385ec366192ac33b70b78f9",
                "NumMedia": "1",
                "MediaUrl0": "https://api.twilio.com/2010-04-01/Accounts/AC736c024b7f0763e7e0268af61611f0d7/Messages/MM4c01e4547385ec366192ac33b70b78f9/Media/ME54e2e31beef6a1b69f27d87311e6a4e7",
                "SmsStatus": "received",
                "AccountSid": "AC736c024b7f0763e7e0268af61611f0d7",
                "ApiVersion": "2010-04-01",
                "MessageSid": "MM4c01e4547385ec366192ac33b70b78f9",
                "NumSegments": "1",
                "ProfileName": "João Mattos",
                "SmsMessageSid": "MM4c01e4547385ec366192ac33b70b78f9",
                "MediaContentType0": "image/jpeg",
            },
            TwilioWebhook(
                To="whatsapp:+14155238886",
                From="whatsapp:+554799930448",
                WaId="554799930448",
                SmsSid="MM4c01e4547385ec366192ac33b70b78f9",
                NumMedia="1",
                MediaUrl0="https://api.twilio.com/2010-04-01/Accounts/AC736c024b7f0763e7e0268af61611f0d7/Messages/MM4c01e4547385ec366192ac33b70b78f9/Media/ME54e2e31beef6a1b69f27d87311e6a4e7",
                SmsStatus=TwilioMessageStatus.RECEIVED,
                AccountSid="AC736c024b7f0763e7e0268af61611f0d7",
                ApiVersion="2010-04-01",
                MessageSid="MM4c01e4547385ec366192ac33b70b78f9",
                NumSegments="1",
                ProfileName="João Mattos",
                SmsMessageSid="MM4c01e4547385ec366192ac33b70b78f9",
                MediaContentType0="image/jpeg",
            ),
        ),
        (
            {
                "To": "whatsapp:+554799930448",
                "From": "whatsapp:+14155238886",
                "SmsSid": "SM9049f8c4ac3e4ab5947cc1dace96a134",
                "SmsStatus": "sent",
                "AccountSid": "AC736c024b7f0763e7e0268af61611f0d7",
                "ApiVersion": "2010-04-01",
                "MessageSid": "SM9049f8c4ac3e4ab5947cc1dace96a134",
                "ChannelPrefix": "whatsapp",
                "MessageStatus": "sent",
                "ChannelToAddress": "+55479993XXXX",
                "ChannelInstallSid": "XEcc20d939f803ee381f2442185d0d5dc5",
                "StructuredMessage": "false",
            },
            TwilioWebhook(
                To="whatsapp:+554799930448",
                From="whatsapp:+14155238886",
                SmsSid="SM9049f8c4ac3e4ab5947cc1dace96a134",
                SmsStatus=TwilioMessageStatus.SENT,
                AccountSid="AC736c024b7f0763e7e0268af61611f0d7",
                ApiVersion="2010-04-01",
                MessageSid="SM9049f8c4ac3e4ab5947cc1dace96a134",
                ChannelPrefix="whatsapp",
                MessageStatus="sent",
                ChannelToAddress="+55479993XXXX",
                ChannelInstallSid="XEcc20d939f803ee381f2442185d0d5dc5",
                StructuredMessage="false",
            ),
        ),
        (
            {
                "To": "whatsapp:+554799930448",
                "From": "whatsapp:+14155238886",
                "SmsSid": "SM9049f8c4ac3e4ab5947cc1dace96a134",
                "SmsStatus": "delivered",
                "AccountSid": "AC736c024b7f0763e7e0268af61611f0d7",
                "ApiVersion": "2010-04-01",
                "MessageSid": "SM9049f8c4ac3e4ab5947cc1dace96a134",
                "ChannelPrefix": "whatsapp",
                "MessageStatus": "delivered",
                "ChannelToAddress": "+55479993XXXX",
                "ChannelInstallSid": "XE55a3fbfcdeb8ecea8cf9100453ab0a4c",
            },
            TwilioWebhook(
                To="whatsapp:+554799930448",
                From="whatsapp:+14155238886",
                SmsSid="SM9049f8c4ac3e4ab5947cc1dace96a134",
                SmsStatus=TwilioMessageStatus.DELIVERED,
                AccountSid="AC736c024b7f0763e7e0268af61611f0d7",
                ApiVersion="2010-04-01",
                MessageSid="SM9049f8c4ac3e4ab5947cc1dace96a134",
                ChannelPrefix="whatsapp",
                MessageStatus="delivered",
                ChannelToAddress="+55479993XXXX",
                ChannelInstallSid="XE55a3fbfcdeb8ecea8cf9100453ab0a4c",
            ),
        ),
        (
            {
                "To": "whatsapp:+554799930448",
                "From": "whatsapp:+14155238886",
                "SmsSid": "SM9049f8c4ac3e4ab5947cc1dace96a134",
                "SmsStatus": "read",
                "AccountSid": "AC736c024b7f0763e7e0268af61611f0d7",
                "ApiVersion": "2010-04-01",
                "MessageSid": "SM9049f8c4ac3e4ab5947cc1dace96a134",
                "ChannelPrefix": "whatsapp",
                "MessageStatus": "read",
                "ChannelToAddress": "+55479993XXXX",
                "ChannelInstallSid": "XE55a3fbfcdeb8ecea8cf9100453ab0a4c",
            },
            TwilioWebhook(
                To="whatsapp:+554799930448",
                From="whatsapp:+14155238886",
                SmsSid="SM9049f8c4ac3e4ab5947cc1dace96a134",
                SmsStatus=TwilioMessageStatus.READ,
                AccountSid="AC736c024b7f0763e7e0268af61611f0d7",
                ApiVersion="2010-04-01",
                MessageSid="SM9049f8c4ac3e4ab5947cc1dace96a134",
                ChannelPrefix="whatsapp",
                MessageStatus="read",
                ChannelToAddress="+55479993XXXX",
                ChannelInstallSid="XE55a3fbfcdeb8ecea8cf9100453ab0a4c",
            ),
        ),
    ],
)
def test_twilio_media_webhook(payload_dict, twilio_webhook):
    assert TwilioWebhook.from_dict(payload_dict) == twilio_webhook