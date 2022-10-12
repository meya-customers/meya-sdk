import pytest

from meya.element.element_test import test_type_registry
from meya.entry import Entry
from meya.event.entry import Event
from meya.gridql.parser import GridQL
from meya.gridql.parser import QueryException
from meya.text.event.ask import AskEvent
from meya.text.event.say import SayEvent
from meya.time.time import from_utc_milliseconds_timestamp
from typing import Optional


@pytest.mark.parametrize(
    ("query", "expected_error"),
    [
        (
            "(a))",
            r"""Query syntax error at ')' in position 3.The value ')' is one of the special characters '+-=&|><!(){}[]^"~*?:\/@', if you would like to include ')' as a literal you can escape it with '\'. Note, for date times you need to quote the date time string e.g. "2020-09-10T12:00:00.500Z".""",
        ),
        ("AND", "Query syntax error at 'AND' in position 0."),
        (
            "[1:2 TO 3]",
            r"""Query syntax error at ':' in position 2.The value ':' is one of the special characters '+-=&|><!(){}[]^"~*?:\/@', if you would like to include ':' as a literal you can escape it with '\'. Note, for date times you need to quote the date time string e.g. "2020-09-10T12:00:00.500Z".""",
        ),
        ("roam~", "Fuzzy matching with ~ is not currently supported"),
        ("jakarta^4 apache", "Unsupported operation type Boost jakarta^4"),
        (
            '"jakarta apache"~10',
            'Unsupported operation type Proximity "jakarta apache"~10',
        ),
        ("+jakarta lucene", "Unsupported operation type Plus +jakarta"),
        (
            '"jakarta apache" -"Apache Lucene"',
            'Unsupported operation type Prohibit -"Apache Lucene"',
        ),
    ],
)
def test_check_error(query: str, expected_error: str):
    with pytest.raises(QueryException) as exc_info:
        GridQL.create(query)
    assert str(exc_info.value) == expected_error


@pytest.mark.parametrize(
    ("data", "query", "expected"), [({}, "", True), ({"foo": "bar"}, "", True)]
)
def test_match_empty(data: dict, query: str, expected: bool):
    gridql = GridQL.create(query)
    assert gridql.match(data) == expected


@pytest.mark.parametrize(
    ("data", "query", "expected"),
    [
        ({"foo": "bar"}, "foo: bar", True),
        ({}, "foo:bar", False),
        ({"foo": "bar"}, "bar", False),
        ({"foo": "bar"}, "foo.bar: baz", False),
        ({"a": {"b": {"c": "d"}}}, "a.b.c: d", True),
        ({"a": {"b": {"c": "e"}}}, "a.b.c: d", False),
        ({"a": {"b": {"e": "d"}}}, "a.b.c: d", False),
        ({"a": {"b": {"c": "d"}}}, "a: (b: (c: d))", True),
        ({"a": {"b": {"c": "e"}}}, "a: (b: (c: d))", False),
        ({"a": {"b": {"e": "d"}}}, "a: (b: (c: d))", False),
        ({"a": {"0": {"b": "c"}, "1": {"d": "e"}}}, "a.0.b: c", True),
        ({"a": {"0": {"b": "f"}, "1": {"d": "e"}}}, "a.0.b: c", False),
        ({"a": [{"b": "c", "d": "e"}]}, "a.0.b: c", False),
    ],
)
def test_match_search_field(data: dict, query: str, expected: bool):
    gridql = GridQL.create(query)
    assert gridql.match(data) == expected


@pytest.mark.parametrize(
    ("data", "query", "expected"),
    [
        ({"type": "bar"}, "type:(b* *r)", True),
        ({"type": "car"}, "type:(b* *r)", False),
        ({"foo": "bar", "pi": 3.14}, "foo:bar AND pi:3.14", True),
        ({"foo": "bar", "pi": 3.14}, "foo:bar pi:3.14", True),
        ({"foo": "bar"}, "foo:bar AND pi:3.14", False),
        ({"type": "bar"}, "type:(a* OR b*)", True),
        ({"type": "car"}, "type:(a* OR b*)", False),
        ({"foo": "bar"}, "foo:(bar OR baz)", True),
        ({"foo": "baz"}, "foo:(bar OR baz)", True),
        ({"foo": "bat"}, "foo:(bar OR baz)", False),
        (
            {"foo": "bar", "pi": 3.14, "fizz": "buzz"},
            "foo:bar pi:3.14 NOT fizz:b?zz",
            False,
        ),
        ({"foo": "bar", "fizz": "buzz"}, "foo:bar AND NOT fizz:buzz", False),
        (
            {"foo": "bar", "fizz": "buzz", "pi": 3.14},
            "(foo:bar AND NOT fizz:b*) OR pi:3.14",
            True,
        ),
    ],
)
def test_match_boolean_ops(data: dict, query: str, expected: bool):
    gridql = GridQL.create(query)
    assert gridql.match(data) == expected


@pytest.mark.parametrize(
    ("data", "query", "expected"),
    [
        (
            {"modified_timestamp": 1600810846508, "text": "hi"},
            "modified_timestamp: [1600810846507 TO 1600810846509]",
            True,
        ),
        ({"foo": 2}, "foo:[1 TO 3]", True),
        ({"foo": [0, 2]}, "foo:[1 TO 3]", True),
        ({"foo": [0, 4]}, "foo:[1 TO 3]", False),
        ({"foo": [[2]]}, "foo:[1 TO 3]", False),
        ({"foo": "2"}, "foo:[1 TO 3]", False),
        ({"foo": None}, "foo:[1 TO 3]", False),
    ],
)
def test_match_range(data: dict, query: str, expected: bool):
    gridql = GridQL.create(query)
    assert gridql.match(data) == expected


@pytest.mark.parametrize(
    ("query", "data", "expected"),
    [
        ("data: *", None, False),
        ("data: purple", "purple", True),
        ("data: purple", "purplex", False),
        ("data: purple", None, False),
        ("data: purple", "Purple", False),
        ('data: "purple people"', "purple people", True),
        ('data: "purple people"', "purple peoplex", False),
        ('data: "purple people"', None, False),
        ('data: "purple people"', "Purple People", False),
        ("data: p*ple", "purple", True),
        ("data: p*\\*ple", "purple", False),
        ("data: p*\\*ple", "pur*ple", True),
        ('data: "p*\\*ple people"', "purple people", False),
        ('data: "p*\\*ple people"', "pur*ple people", True),
        ("data: p?ple", "purple", False),
        ("data: p??ple", "purple", True),
        ("data: *people*", "I like people!", True),
        ("data: people*", "I like people!", False),
        ("data: meya.text.*", "meya.text.event.say", True),
        ("data: purple", ["purple", "yellow"], True),
        ("data: purple", [False, None, "yellow", "purple"], True),
        ("data: p??ple", ["yellow", "purple"], True),
        ("data: purple", [], False),
        ("data: purple", ["blue", "red"], False),
        ("data: p??ple", [["purple"]], False),
        ("data: 10", 10, True),
        ("data: 1*", 10, True),
        ("data: 3.14", 3.14, True),
        ("data: true", True, True),
        ("data: false", False, True),
        ("data: /[abc]+/", "aabbcc", True),
        ("data: /[abc]+/", "aabbccd", False),
        ("data: /[abc]+/", "", False),
        ("data: /[abc]+/", "adbc", False),
    ],
)
def test_match_term(query: str, data: str, expected: bool):
    assert GridQL.create(query).match({"data": data}) == expected


@pytest.mark.parametrize(
    ("entry", "query", "expected"),
    [
        (SayEvent(text="hi"), "meya.event.entry", True),
        (SayEvent(text="hi"), "meya.text.event", True),
        (SayEvent(text="hi"), "meya.event.entry NOT meya.text.event", False),
        (SayEvent(text="hi"), "type:meya.text.event", True),
        (AskEvent(text="hi"), "meya.text.event", True),
        (SayEvent(text="hi"), "meya.text.event AND text:hi", True),
        (
            SayEvent(text="hi"),
            "type:meya.text.event.say AND NOT text:hi",
            False,
        ),
        (SayEvent(text="hi"), "NOT meya.text.event.say", False),
        (AskEvent(text="hi"), "NOT type:meya.text.event.say", True),
        (
            SayEvent(text="hi"),
            "meya.text.event.say OR meya.text.event.ask",
            True,
        ),
        (AskEvent(text="hi"), "meya.event.entry.interactive", True),
        (
            SayEvent(text="I like purple pumpkins"),
            "meya.text.event AND text:*p??ple*",
            True,
        ),
    ],
)
def test_match_entry_type(entry: Entry, query: str, expected: bool):
    entry.entry_id = "1600810846508-0"
    assert (
        GridQL.create(query, type_registry=test_type_registry).match_entry(
            entry
        )
        == expected
    )


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (
            '["2020-09-22T21:40:46.400000+00:00" TO "2020-09-22T21:40:46.600000+00:00"]',
            True,
        ),
        (
            '["2020-09-22T21:40:46.400000+00:00" TO "2020-09-22T21:40:46.500000+00:00"]',
            False,
        ),
        (
            'meya.text.event AND text:*p??ple* AND ["2020-09-22T21:40:46.400000+00:00" TO "2020-09-22T21:40:46.600000+00:00"]',
            True,
        ),
        (
            'meya.text.event AND text:*p??ple* AND ["2020-09-22T21:40:46.400000+00:00" TO "2020-09-22T21:40:46.500000+00:00"]',
            False,
        ),
        (
            'meya.text.event AND text:*p??ple* OR ["2020-09-22T21:40:46.400000+00:00" TO "2020-09-22T21:40:46.500000+00:00"]',
            True,
        ),
        ("[1600810846508 TO 1600810846508]", True),
        ("{1600810846508 TO 1700810846508]", False),
        ("[1500810846508 TO 1600810846508}", False),
    ],
)
def test_match_entry_timestamp(query: str, expected: bool):
    entry = SayEvent(text="I like purple pumpkins")
    entry.entry_id = "1600810846508-0"
    assert (
        GridQL.create(query, type_registry=test_type_registry).match_entry(
            entry
        )
        == expected
    )


@pytest.mark.parametrize(
    ("entry_type", "expected_error"),
    [
        ("INVALID_TYPE", "Invalid reference to entry type `INVALID_TYPE`"),
        ("meya.text.event.say", None),
        (
            "meya.text.event.sayx",
            "Invalid reference to entry type `meya.text.event.sayx`",
        ),
        ("meya.event.entry.interactive", None),
        (
            "meya.text.event.*",
            "Invalid operation meya.text.event.*. Wildcard not supported here.",
        ),
    ],
)
def test_entry_type_error(entry_type: str, expected_error: Optional[str]):
    query = f"{entry_type} AND text:bar*"
    gridql = GridQL.create(query, type_registry=test_type_registry)
    try:
        event = Event()
        event.entry_id = "1600810846508-0"
        gridql.match_entry(event)
        message = None
    except QueryException as e:
        message = str(e)
    assert message == expected_error
