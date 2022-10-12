import pytest

from meya.util.json import from_json
from meya.util.json import to_json


@pytest.mark.parametrize(
    ("text", "obj"),
    [
        ("[1,2,3]", [1, 2, 3]),
        (
            '{"sendgrid_email_address":"test🤯@sendgrid.meya.ai"}',
            {"sendgrid_email_address": "test🤯@sendgrid.meya.ai"},
        ),
    ],
)
def test_load_and_dump(text, obj):
    assert from_json(text) == obj
    assert to_json(obj) == text
