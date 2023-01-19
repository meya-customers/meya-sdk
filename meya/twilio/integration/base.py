from colored import attr
from colored import fg
from dataclasses import dataclass
from meya import env
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.integration.element import Integration
from typing import ClassVar
from typing import Optional
from typing import Type


@dataclass
class TwilioBaseIntegration(Integration):
    is_abstract: bool = meta_field(value=True)

    account_sid: str = element_field(
        help="Twilio project Account SID.", meta_name="account SID"
    )
    auth_token: Optional[str] = element_field(
        default=None,
        help=(
            "Twilio project auth token. "
            "This field is being deprecated, switch to api_key_sid and "
            "api_key_secret as soon as possible. "
            "For more information, "
            "see https://www.twilio.com/console/project/api-keys"
        ),
    )
    api_key_sid: Optional[str] = element_field(
        default=None,
        help=(
            "Twilio API Key SID. "
            "Access https://www.twilio.com/console/project/api-keys to manage "
            "API Keys."
        ),
    )
    api_key_secret: Optional[str] = element_field(
        default=None,
        help=(
            "Twilio API Key secret. "
            "Access https://www.twilio.com/console/project/api-keys to manage "
            "API Keys."
        ),
    )
    phone_number: Optional[str] = element_field(
        default=None,
        help=(
            "Twilio active number for use with Meya. Note, this can also be a "
            "Message Service ID. For SMS/calls this will generally be a "
            "standard E.164 number e.g. +15554440000. For WhatsApp this "
            "needs to be a prefixed E.164 number e.g. "
            "whatsapp:+15554440000. For a message service, you just use the "
            "Message Service ID directly "
            "e.g. MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX."
        ),
    )

    def validate(self):
        super().validate()
        if (
            not self.auth_token
            and not self.api_key_secret
            and not self.api_key_sid
        ):
            raise self.validation_error(
                "You need to provide the `api_key_secret` and `api_key_sid` "
                "to use the Twilio integration. "
                "For more information, see "
                "https://www.twilio.com/console/project/api-keys"
            )
        if self.auth_token and not env.cluster_type:
            print(
                f"{fg('light_salmon_3b') + attr('bold')}"
                f"w {self.id} authentication via auth token is being "
                f"deprecated. Switch to API Key as soon as possible. "
                "For more information, see "
                "https://www.twilio.com/console/project/api-keys"
            )


class TwilioBaseIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = TwilioBaseIntegration
