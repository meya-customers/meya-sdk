import json

from typing import Any
from typing import Union


def from_json(stream: Union[str, bytes, bytearray]) -> Any:
    return json.loads(stream)


def to_json(obj: Any, pretty: bool = False) -> str:
    if pretty:
        indent = 4
        separators = (", ", ": ")
    else:
        indent = None
        separators = (",", ":")
    return json.dumps(
        obj, ensure_ascii=False, indent=indent, separators=separators
    )
