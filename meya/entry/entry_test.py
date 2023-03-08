import pytest
import pytz

from datetime import datetime
from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import test_type_registry
from meya.element.element_test import to_spec_dict
from meya.entry import Entry
from meya.entry.entry import EntryRef
from meya.event.composer_spec import ComposerEventSpec
from meya.event.entry import Event
from meya.event.header_spec import HeaderEventSpec
from meya.text.component.say import SayComponent
from meya.text.event.say import SayEvent


def test_entry_timestamp():
    entry = SayEvent(user_id="U0", text=".", thread_id="T0")
    entry.entry_id = "930293840-1"
    assert entry.entry_milliseconds_timestamp == 930293840


def test_entry_decrement_entry_id():
    entry = SayEvent(
        composer=ComposerEventSpec(),
        user_id="U0",
        quick_replies=[],
        text=".",
        thread_id="T0",
    )
    entry.entry_id = "930293840-1"
    assert entry.decremented_entry_id == "930293840-0"
    entry.entry_id = "930293840-0"
    assert entry.decremented_entry_id == "930293839"


@pytest.mark.parametrize(
    ("subclass", "entry_type"),
    [
        (Event, "meya.event.entry"),
        (SayEvent, "meya.text.event.say"),
        (ComponentStartEntry, "meya.component.entry.start"),
    ],
)
def test_get_entry_type(subclass, entry_type):
    assert subclass.get_entry_type(test_type_registry) == entry_type


@pytest.mark.parametrize(
    ("subclass", "entry_ledger"),
    [(Event, "event"), (SayEvent, "event"), (ComponentStartEntry, "bot")],
)
def test_get_entry_ledger(subclass, entry_ledger):
    assert subclass.get_entry_ledger() == entry_ledger


@pytest.mark.parametrize(
    ("entry", "typed_dict"),
    [
        (
            SayEvent(
                composer=ComposerEventSpec(),
                context={},
                user_id="O123",
                quick_replies=[],
                header=HeaderEventSpec(),
                markdown=[],
                text="T456",
                thread_id="T0",
                trace_id="xyz",
                parent_entry_ref=EntryRef(
                    ledger="bot", id="23-0", data=dict(thread_id="T0")
                ),
            ),
            {
                "type": "meya.text.event.say",
                "data": {
                    "composer": {},
                    "markdown": [],
                    "parent_entry_ref": {
                        "ledger": "bot",
                        "id": "23-0",
                        "data": {"thread_id": "T0"},
                    },
                    "quick_replies": [],
                    "header": {},
                    "text": "T456",
                    "thread_id": "T0",
                    "trace_id": "xyz",
                    "user_id": "O123",
                },
            },
        )
    ],
)
def test_from_typed_dict(entry, typed_dict):
    assert Entry.from_typed_dict(typed_dict, test_type_registry) == entry


@pytest.mark.parametrize(
    ("entry", "entry_id", "typed_dict"),
    [
        (
            SayEvent(
                composer=ComposerEventSpec(),
                context={},
                user_id="O123",
                quick_replies=[],
                header=HeaderEventSpec(),
                markdown=[],
                text="T456",
                thread_id="T0",
                trace_id="xyz",
                parent_entry_ref=EntryRef(
                    ledger="bot",
                    id="23-0",
                    data=dict(bot_id="B1", thread_id="T0"),
                ),
            ),
            None,
            {
                "type": "meya.text.event.say",
                "data": {
                    "composer": {},
                    "context": {},
                    "markdown": [],
                    "parent_entry_ref": {
                        "ledger": "bot",
                        "id": "23-0",
                        "data": {"bot_id": "B1", "thread_id": "T0"},
                    },
                    "quick_replies": [],
                    "header": {},
                    "sensitive": False,
                    "internal": False,
                    "text": "T456",
                    "thread_id": "T0",
                    "trace_id": "xyz",
                    "user_id": "O123",
                },
            },
        ),
        (
            SayEvent(
                composer=ComposerEventSpec(),
                context={},
                user_id="O123",
                quick_replies=[],
                header=HeaderEventSpec(),
                markdown=[],
                text="",
                thread_id="T0",
                trace_id="xyz",
                parent_entry_ref=EntryRef(
                    ledger="bot",
                    id="23-0",
                    data=dict(bot_id="B1", thread_id="T0"),
                ),
            ),
            None,
            {
                "type": "meya.text.event.say",
                "data": {
                    "composer": {},
                    "context": {},
                    "markdown": [],
                    "parent_entry_ref": {
                        "ledger": "bot",
                        "id": "23-0",
                        "data": {"bot_id": "B1", "thread_id": "T0"},
                    },
                    "quick_replies": [],
                    "header": {},
                    "sensitive": False,
                    "internal": False,
                    "text": "",
                    "thread_id": "T0",
                    "trace_id": "xyz",
                    "user_id": "O123",
                },
            },
        ),
        (
            ComponentStartEntry(
                bot_id="grid_bot",
                data={"K5": "V4", "K84": "V11"},
                flow="F123",
                index=2,
                spec=to_spec_dict(SayComponent(say="hi")),
                stack=[],
                thread_id="T0",
                trace_id="xyz",
                parent_entry_ref=EntryRef(
                    ledger="bot",
                    id="23-0",
                    data=dict(bot_id="B1", thread_id="T0"),
                ),
            ),
            "123-0",
            {
                "id": "123-0",
                "type": "meya.component.entry.start",
                "data": {
                    "bot_id": "grid_bot",
                    "data": {"K5": "V4", "K84": "V11"},
                    "flow": "F123",
                    "index": 2,
                    "parent_entry_ref": {
                        "ledger": "bot",
                        "id": "23-0",
                        "data": {"bot_id": "B1", "thread_id": "T0"},
                    },
                    "sensitive": False,
                    "internal": False,
                    "spec": {
                        "data": {
                            "composer": {},
                            "context": {},
                            "say": "hi",
                            "sensitive": False,
                            "quick_replies": [],
                            "header": {},
                            "triggers": [],
                        },
                        "type": "meya.text.component.say",
                    },
                    "stack": [],
                    "thread_id": "T0",
                    "trace_id": "xyz",
                },
            },
        ),
    ],
)
def test_to_from_typed_dict(entry, entry_id, typed_dict):
    entry.entry_id = entry_id
    assert entry.to_typed_dict(test_type_registry) == typed_dict, "to"
    assert (
        Entry.from_typed_dict(typed_dict, test_type_registry) == entry
    ), "from"
    assert (
        Entry.from_typed_dict(typed_dict, test_type_registry).to_typed_dict(
            test_type_registry
        )
        == typed_dict
    ), "from then to"
    assert (
        Entry.from_typed_dict(
            entry.to_typed_dict(test_type_registry), test_type_registry
        )
        == entry
    ), "to then from"


def test_get_entry_id():
    entry_timestamp = datetime(
        year=2020,
        month=9,
        day=4,
        hour=21,
        minute=35,
        second=54,
        microsecond=675000,
        tzinfo=pytz.utc,
    )
    entry_sequence = 1
    entry_id = Entry.get_entry_id(entry_timestamp, entry_sequence)
    assert entry_id == "1599255354675-1"
