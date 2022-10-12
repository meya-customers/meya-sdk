from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconElementSpecUnion
from meya.integration.element import Integration
from typing import ClassVar
from typing import Type
from typing import Union


@dataclass
class DialogflowIntegration(Integration):
    NAME: ClassVar[str] = "dialogflow"

    meta_icon: IconElementSpecUnion = meta_field(
        value=IconElementSpec(
            url="https://meya-website.cdn.prismic.io/meya-website/175d925e-6a3a-4c27-b13c-04fe955d1a25_dialogflow.svg"
        )
    )

    service_account_key: Union[str, dict] = element_field()

    async def accept(self) -> bool:
        return False


class DialogflowIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = DialogflowIntegration
