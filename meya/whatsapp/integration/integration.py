from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconElementSpecUnion
from meya.twilio.integration import TwilioIntegration
from typing import ClassVar
from typing import Type


@dataclass
class WhatsAppIntegration(TwilioIntegration):
    NAME: ClassVar[str] = "whatsapp"
    mark_incoming_as_read: ClassVar[bool] = True

    meta_name: str = meta_field(value="WhatsApp")
    meta_icon: IconElementSpecUnion = meta_field(
        value=IconElementSpec(
            url="https://meya-website.cdn.prismic.io/meya-website/0decb67d-e3ec-4f66-a1f8-135e19a3bcdf_whatsapp.svg"
        )
    )


class WhatsAppIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = TwilioIntegration
