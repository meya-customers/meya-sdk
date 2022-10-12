import pytest

from meya.util.msgpack import from_msgpack
from meya.util.msgpack import to_msgpack


@pytest.mark.parametrize(
    "obj",
    [
        None,
        "",
        "abc",
        0,
        1,
        -1,
        0.0,
        1.0,
        -1.0,
        float("inf"),
        -float("inf"),
        [],
        ["q", "z"],
        {},
        {"type": "x", "data": {"a": 1}},
    ],
)
def test_encode_decode(obj):
    result = from_msgpack(to_msgpack(obj))
    assert result == obj
    assert type(result) is type(obj)


@pytest.mark.parametrize(
    ("obj", "expected_result"),
    [
        (b"123", "123"),
        ([1, "2", b"3"], [1, "2", "3"]),
        ({"key": b"value"}, {"key": "value"}),
    ],
)
def test_parse_binary_as_string(obj, expected_result):
    result = from_msgpack(to_msgpack(obj))
    assert result == expected_result
