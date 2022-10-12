from dataclasses import MISSING
from dataclasses import dataclass
from meya.util.dict import dataclass_field_default
from meya.util.dict import dataclass_init_fields
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Any
from typing import ClassVar
from typing import Dict


class PayloadError(Exception):
    pass


@dataclass
class Payload:
    preserve_nones: ClassVar[bool] = False
    to_camel_case_fields: ClassVar[bool] = False
    from_camel_case_fields: ClassVar[bool] = False

    def __repr__(self):
        args = []
        for field in dataclass_init_fields(self.__class__):
            if field.repr:
                value = getattr(self, field.name)
                default, default_factory = dataclass_field_default(field)
                if not (
                    (default is not MISSING and value == default)
                    or (
                        default_factory is not MISSING
                        and value == default_factory()
                    )
                ):
                    args.append((field.name, value))
        return f'{self.__class__.__qualname__}({", ".join(f"{arg[0]}={arg[1]!r}" for arg in args)})'

    @classmethod
    def from_dict(cls, payload_dict: Dict[str, Any]) -> "Payload":
        try:
            return from_dict(
                cls,
                payload_dict,
                from_camel_case_fields=cls.to_camel_case_fields,
            )
        except ValueError as e:
            raise PayloadError(repr(e))

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(
            self,
            preserve_nones=self.preserve_nones,
            to_camel_case_fields=self.to_camel_case_fields,
        )
