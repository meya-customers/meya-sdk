import meya.util.uuid
import re

from unittest.mock import patch


def patch_uuid4_hex():
    counter = 0

    def incr_hex():
        nonlocal counter
        value = f"~{counter:x}"
        counter += 1
        return value

    return patch(new=incr_hex, target="meya.util.uuid.uuid4_hex")


@patch_uuid4_hex()
def test_patch_uuid4_hex():
    assert meya.util.uuid.uuid4_hex() == "~0"
    assert meya.util.uuid.uuid4_hex() == "~1"


def test_uuid4_hex():
    assert re.match(r"^[0-9a-f]{32}$", meya.util.uuid.uuid4_hex()) is not None
