from dataclasses import dataclass
from meya.component.element import Component
from meya.component.entry import ComponentEntry
from meya.db.view.thread import ThreadView
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.flow.entry import FlowEntry
from meya.util.dict import dataclass_get_meta_value
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from meya.util.enum import SimpleEnum
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Type
from typing import TypeVar


class EventConfigScope(SimpleEnum):
    THREAD = "thread"
    FLOW = "flow"


T = TypeVar("T")


class EventConfig(Generic[T]):
    key: ClassVar[str]
    type: ClassVar[Type[T]]

    @classmethod
    def get(cls) -> T:
        entry = Entry.current.get()
        if isinstance(entry, (FlowEntry, ComponentEntry)):
            current = entry.data.get(cls.key)
            flow_value = from_dict(cls.type, current)
        else:
            flow_value = None
        thread = ThreadView.current.get()
        thread_value = from_dict(cls.type, thread[cls.key])
        if hasattr(flow_value, "__or__") and thread_value is not None:
            return flow_value | thread_value
        else:
            return flow_value or thread_value


@dataclass
class EventConfigComponent(Component):
    is_abstract: bool = meta_field(value=True)
    config: Type[EventConfig] = meta_field()
    scope: EventConfigScope = element_field(default=EventConfigScope.THREAD)

    async def start(self) -> List[Entry]:
        value = to_dict(self.get_component_value())
        config = self.get_meta_config()
        if self.scope == EventConfigScope.FLOW:
            return self.respond(data={config.key: value})
        else:
            self.thread[config.key] = value
            return self.respond()

    def get_component_value(self) -> Any:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    @classmethod
    def get_meta_config(cls) -> EventConfig:
        return dataclass_get_meta_value(cls, "config")
