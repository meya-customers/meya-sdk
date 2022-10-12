import pytest

from meya.util.camel_case import from_camel_case
from meya.util.camel_case import from_camel_case_dict_keys
from meya.util.camel_case import to_camel_case
from meya.util.camel_case import to_camel_case_dict_keys


@pytest.mark.parametrize(
    ("original", "camel_case"),
    [("a_b_c", "aBC"), ("abc", "abc"), ("abc_def", "abcDef")],
)
def test_round_trip(original: str, camel_case: str):
    assert to_camel_case(original) == camel_case
    assert from_camel_case(camel_case) == original

    result = from_camel_case(to_camel_case(original))
    assert result == original

    result = to_camel_case(from_camel_case(camel_case))
    assert result == camel_case


@pytest.mark.parametrize(
    ("original", "camel_case"),
    [
        (
            {"a_b_c": {"abc": {"abc_def": 0}}, 1: 1},
            {"aBC": {"abc": {"abcDef": 0}}, 1: 1},
        )
    ],
)
def test_dict_keys_round_trip(original: dict, camel_case: dict):
    assert to_camel_case_dict_keys(original) == camel_case
    assert from_camel_case_dict_keys(camel_case) == original

    result = from_camel_case_dict_keys(to_camel_case_dict_keys(original))
    assert result == original

    result = to_camel_case_dict_keys(from_camel_case_dict_keys(camel_case))
    assert result == camel_case
