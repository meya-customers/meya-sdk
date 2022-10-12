import msgpack

from typing import Any

# Use MessagePack 1.0 "raw" for both binary and Unicode (Redis Lua compat)
_PACKER_KWARGS = dict(use_bin_type=False)
_UNPACKER_KWARGS = dict(raw=False)


class Packer(msgpack.Packer):
    def __init__(self, *, lua_mode: bool = False):
        super().__init__(**_PACKER_KWARGS)


class Unpacker(msgpack.Unpacker):
    def __init__(self):
        super().__init__(**_UNPACKER_KWARGS)


def to_msgpack(obj: Any) -> bytes:
    return Packer().pack(obj)


def from_msgpack(data: bytes) -> Any:
    return msgpack.unpackb(data, **_UNPACKER_KWARGS)
