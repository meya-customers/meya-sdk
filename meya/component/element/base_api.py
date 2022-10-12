from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import element_field
from meya.element.field import meta_field


@dataclass
class BaseApiComponent(Component):
    is_abstract: bool = meta_field(value=True)

    sensitive: bool = element_field(default=True)
