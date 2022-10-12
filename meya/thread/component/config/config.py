from dataclasses import dataclass
from meya.component.element import Component
from meya.db.view.thread import ThreadView
from meya.element.field import meta_field
from meya.entry import Entry
from meya.util.dict import dataclass_get_meta_value
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Type
from typing import TypeVar

T = TypeVar("T")


class ThreadConfig(Generic[T]):
    key: ClassVar[str]
    type: ClassVar[Type[T]]

    @classmethod
    def set(cls, value: T) -> None:
        thread = ThreadView.current.get()
        thread[cls.key] = to_dict(value)

    @classmethod
    def get(cls) -> T:
        thread = ThreadView.current.get()
        return from_dict(cls.type, thread[cls.key])


@dataclass
class ThreadConfigComponent(Component):
    is_abstract: bool = meta_field(value=True)
    config: Type[ThreadConfig] = meta_field()

    async def start(self) -> List[Entry]:
        value = to_dict(self.get_component_value())
        config = self.get_meta_config()
        self.thread[config.key] = value
        return self.respond()

    def get_component_value(self) -> Any:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    @classmethod
    def get_meta_config(cls) -> ThreadConfig:
        return dataclass_get_meta_value(cls, "config")
