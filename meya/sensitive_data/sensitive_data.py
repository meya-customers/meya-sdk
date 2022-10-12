from base64 import b85decode
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

REDACTED_TEXT = "⭑⭑⭑⭑⭑⭑"

sensitive_KEYIDBYTES = 16  # use 128 bits, same as UUIDv4


@dataclass
class SensitiveDataRef:
    ref_key_value: str = field(metadata=dict(key="🔐🙈"))

    _ref_key_id_bytes: Optional[bytes] = field(
        init=False, compare=False, default=None, repr=False
    )
    _ref_key_bytes: Optional[bytes] = field(
        init=False, compare=False, default=None, repr=False
    )

    @property
    def ref_key_id_bytes(self) -> bytes:
        self._decode()
        return self._ref_key_id_bytes

    @property
    def ref_key_bytes(self) -> bytes:
        self._decode()
        return self._ref_key_bytes

    def _decode(self) -> None:
        if self._ref_key_id_bytes is None or self._ref_key_bytes is None:
            combined_bytes = b85decode(self.ref_key_value)
            self._ref_key_id_bytes = combined_bytes[:sensitive_KEYIDBYTES]
            self._ref_key_bytes = combined_bytes[sensitive_KEYIDBYTES:]
