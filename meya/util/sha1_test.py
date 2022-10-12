import pytest

from meya.util.sha1 import sha1_hex


@pytest.mark.parametrize(
    ("data", "expected_sha1"),
    [
        ((b"",), "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        ((b"abc",), "a9993e364706816aba3e25717850c26c9cd0d89d"),
        ((b"a", b"b", b"c"), "a9993e364706816aba3e25717850c26c9cd0d89d"),
        (("abc",), "a9993e364706816aba3e25717850c26c9cd0d89d"),
        ((b"a", "b", b"c"), "a9993e364706816aba3e25717850c26c9cd0d89d"),
        ((b"\x93\x01\x02\x03",), "78a74af6c06029985f388dfeceb9794100377124"),
        (([],), "c4595d8f743731cbc1ca0bb34be79a40d771ddf0"),
        ((1,), "bf8b4530d8d246dd74ac53a13471bba17941dff7"),
        (({"a": 1, "b": 2},), "befd7e40e2f0ccb6158f05022b398a0e02afb8b1"),
    ],
)
def test_sha1_hex(data, expected_sha1):
    sha1 = sha1_hex(*data)
    assert sha1 == expected_sha1
