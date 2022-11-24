from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
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
    enable_rich_content: bool = element_field(
        default=False,
        help=(
            "Use the Twilio Content API to render quick replies and list "
            "pickers in WhatsApp. "
            "Note, WhatsApp only allows a maximum of 3 quick replies for a "
            "message, therefore the integration will always truncate the "
            "set of Meya quick replies or buttons to the first 3 items."
        ),
    )
    list_picker_default_text: str = element_field(
        default="...",
        help=(
            "The default text for the list picker widget. This is only used "
            "if the `ask` property is not set in the ask button component."
        ),
    )
    list_picker_default_button_text: str = element_field(
        default="Select",
        help=(
            "The default button text for the list picker widget. This is only "
            "used if the `label` property is not set in the adk button "
            "component."
        ),
    )


class WhatsAppIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = TwilioIntegration
