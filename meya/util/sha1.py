from hashlib import sha1
from meya.util.msgpack import to_msgpack
from typing import Any


def sha1_hex(*data: Any) -> str:
    new_hash = sha1()
    for item in data:
        if isinstance(item, str):
            item = item.encode("utf-8")
        elif not isinstance(item, bytes):
            item = to_msgpack(item)
        new_hash.update(item)
    return new_hash.hexdigest()
