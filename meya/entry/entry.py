from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from meya.core.abstract_type_registry import AbstractTypeRegistry
from meya.entry.field import entry_field
from meya.time.time import from_utc_milliseconds_timestamp
from meya.time.time import to_utc_milliseconds_timestamp
from meya.util.context_var import ScopedContextVar
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import cast


@dataclass
class EntryRef:
    ledger: str
    id: str
    data: Dict[str, str]


@dataclass
class Entry(ABC):
    entry_id: Optional[str] = field(init=False, default=None)

    parent_entry_ref: Optional[EntryRef] = entry_field(
        default=None, default_missing=True
    )
    trace_id: str = entry_field(default="-", default_missing=True)
    sensitive: bool = entry_field(default=False)

    current: ClassVar = cast(ScopedContextVar["Entry"], ScopedContextVar())
    current_encrypted: ClassVar = cast(
        ScopedContextVar["Entry"], ScopedContextVar("encrypted")
    )
    current_redacted: ClassVar = cast(
        ScopedContextVar["Entry"], ScopedContextVar("redacted")
    )

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Entry":
        return from_dict(cls, obj)

    @classmethod
    @abstractmethod
    def get_entry_ledger(cls) -> str:
        pass

    @classmethod
    def get_entry_type(
        cls, type_registry: Optional[AbstractTypeRegistry] = None
    ) -> str:
        return (
            type_registry or AbstractTypeRegistry.current.get()
        ).reverse_alias[cls]

    @classmethod
    def from_typed_dict(
        cls,
        entry_dict: Dict[str, Any],
        type_registry: Optional[AbstractTypeRegistry] = None,
    ):
        entry_type = entry_dict["type"]
        entry_data = entry_dict["data"]
        entry_id = entry_dict.get("id")
        subclass = cls.get_entry_type_subclass(entry_type, type_registry)
        try:
            entry = subclass.from_dict(entry_data)
        except ValueError:
            raise ValueError(f"Cannot convert {entry_type} from {entry_data}")
        entry.entry_id = entry_id
        return entry

    @classmethod
    def try_get_entry_type_subclass(
        cls,
        entry_type: str,
        type_registry: Optional[AbstractTypeRegistry] = None,
    ) -> Optional[Type["Entry"]]:
        subclass = (
            type_registry or AbstractTypeRegistry.current.get()
        ).alias.get(entry_type)
        if subclass and issubclass(subclass, cls):
            return subclass
        else:
            return None

    @classmethod
    def get_entry_type_subclass(
        cls,
        entry_type: str,
        type_registry: Optional[AbstractTypeRegistry] = None,
    ) -> Type["Entry"]:
        subclass = cls.try_get_entry_type_subclass(entry_type, type_registry)
        assert subclass is not None, f"No such entry type {entry_type}"
        return subclass

    @classmethod
    def get_all_entry_type_subclasses(
        cls, type_registry: AbstractTypeRegistry
    ) -> List[Type["Entry"]]:
        return [
            subclass
            for subclass in type_registry.items
            if issubclass(subclass, cls)
        ]

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)

    def to_typed_dict(
        self, type_registry: Optional[AbstractTypeRegistry] = None
    ) -> Dict[str, Any]:
        result = {}
        result["type"] = self.get_entry_type(type_registry)
        result["data"] = self.to_dict()
        if self.entry_id:
            result["id"] = self.entry_id
        return result

    @property
    def entry_milliseconds_timestamp(self) -> int:
        return int(self.entry_id.split("-")[0]) if self.entry_id != "*" else 0

    @property
    def entry_posix_timestamp(self) -> float:
        return self.entry_milliseconds_timestamp / 1000

    @property
    def decremented_entry_id(self) -> str:
        return self.get_decremented_entry_id(self.entry_id)

    @staticmethod
    def get_decremented_entry_id(entry_id: str) -> str:
        [time_part, sequence_part] = [
            int(part) for part in entry_id.split("-")
        ]
        if sequence_part > 0:
            return f"{time_part}-{sequence_part - 1}"
        else:
            return f"{time_part - 1}"

    @property
    def incremented_entry_id(self) -> str:
        return self.get_incremented_entry_id(self.entry_id)

    @staticmethod
    def get_incremented_entry_id(entry_id: str) -> str:
        [time_part, sequence_part] = [
            int(part) for part in entry_id.split("-")
        ]
        return f"{time_part}-{sequence_part + 1}"

    @property
    def entry_ledger(self) -> str:
        return self.get_entry_ledger()

    @abstractmethod
    def to_ref(self) -> EntryRef:
        pass

    @property
    def entry_timestamp_and_seq(self) -> Tuple[datetime, int]:
        return self.get_timestamp_and_seq(self.entry_id)

    @staticmethod
    def get_timestamp_and_seq(entry_id: str) -> Tuple[datetime, int]:
        (ts, seq) = entry_id.split("-")
        return from_utc_milliseconds_timestamp(int(ts)), int(seq)

    @staticmethod
    def get_entry_id(entry_timestamp: datetime, entry_sequence: int) -> str:
        return f"{to_utc_milliseconds_timestamp(entry_timestamp)}-{entry_sequence}"
