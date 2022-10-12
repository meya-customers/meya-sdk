from dataclasses import dataclass
from meya.component.entry.next import ComponentNextEntry
from meya.component.entry.start import ComponentStartEntry
from meya.component.meta_tag import ActionComponentTag
from meya.core.meta_tag import MetaTag
from meya.element import Element
from meya.element import Spec
from meya.element.field import meta_field
from meya.element.field import process_field
from typing import ClassVar
from typing import List
from typing import Type
from typing import Union


@dataclass
class AbstractComponent(Element):
    is_abstract: bool = meta_field(value=True)

    entry: Union[ComponentStartEntry, ComponentNextEntry] = process_field()


@dataclass
class ComponentSpec(Spec):
    element_type: ClassVar[Type[Element]] = AbstractComponent

    snippet_default: str = meta_field(value="next")


@dataclass
class FlowComponentSpec(ComponentSpec):
    meta_name: str = meta_field(value="Component")
    snippet_default: str = meta_field(value="next")


@dataclass
class ActionComponentSpec(ComponentSpec):
    meta_name: str = meta_field(value="Component")
    snippet_default: str = meta_field(value="next")
    top_level_minimum: float = meta_field(value=0.6)
    top_level_tags: List[Type[MetaTag]] = meta_field(
        value=[ActionComponentTag]
    )
