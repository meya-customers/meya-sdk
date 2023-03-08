from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconElementSpecUnion
from meya.integration.element import Integration
from typing import ClassVar
from typing import Optional
from typing import Type


@dataclass
class OpenaiIntegration(Integration):
    NAME: ClassVar[str] = "openai"

    meta_icon: IconElementSpecUnion = meta_field(
        value=IconElementSpec(
            url="https://meya-website.cdn.prismic.io/meya-website/175d925e-6a3a-4c27-b13c-04fe955d1a25_dialogflow.svg"
        )
    )

    api_key: Optional[str] = element_field(
        default=None,
        help=(
            "The OpenAI API key to use for this integration. If not provided, "
            "the integration will use Meya's OpenAI API key for all requests. "
            "You will be charged for any requests made using Meya's API key "
            "according to Meya's token usage rates."
        ),
    )

    async def accept(self) -> bool:
        return False


class OpenaiIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = OpenaiIntegration
