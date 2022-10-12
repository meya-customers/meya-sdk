from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpecUnion
from typing import ClassVar
from typing import Type


class LogElement(Element):
    is_abstract: bool = meta_field(value=True)
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/09-shopping-ecommerce/04-receipts/receipt-1.svg"
    )


class LogSpec(Spec):
    element_type: ClassVar[Type[Element]] = LogElement


class LogRef(Ref):
    element_type: ClassVar[Type[Element]] = LogElement
