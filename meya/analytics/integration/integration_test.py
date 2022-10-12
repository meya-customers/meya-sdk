import pytest

from meya.analytics.integration import AnalyticsIntegration
from meya.button.event.click import ButtonClickEvent
from meya.component.entry.start import ComponentStartEntry
from meya.core.type_registry import TypeRegistry
from meya.element.element_error import ElementValidationError
from meya.element.element_test import test_type_registry
from meya.entry import Entry
from meya.event.composer_spec import ComposerEventSpec
from meya.http.entry.request import HttpRequestEntry
from meya.text.component.say import SayComponent
from meya.text.event.say import SayEvent
from meya.thread.entry.data import ThreadDataEntry
from meya.user.entry.data import UserDataEntry
from typing import List
from typing import Optional


class MockAnalyticsIntegration(AnalyticsIntegration):
    async def identify(self) -> HttpRequestEntry:
        pass

    async def track(self) -> HttpRequestEntry:
        pass


@pytest.mark.parametrize(
    ("whitelist", "blacklist", "validation_message"),
    [
        ([], [], None),
        (["foo", "abc"], [], None),
        ([], ["foo", "abc"], None),
        (
            ["xyz"],
            ["foo", "abc"],
            "only either tracked or untracked user data is supported",
        ),
    ],
)
def test_validate_user_data_whitelist_blacklist(
    whitelist: List[str],
    blacklist: List[str],
    validation_message: Optional[str],
):
    element = MockAnalyticsIntegration(
        track_user_data=True,
        tracked_user_data=whitelist,
        untracked_user_data=blacklist,
    )
    if validation_message:
        with pytest.raises(ElementValidationError) as excinfo:
            element.validate()
        assert str(excinfo.value) == validation_message
    else:
        element.validate()


@pytest.mark.parametrize(
    ("whitelist", "blacklist", "validation_message"),
    [
        ([], [], None),
        (["foo"], [], 'invalid tracked entry "foo"'),
        (
            [SayComponent.get_element_type(test_type_registry)],
            [],
            'invalid tracked entry "meya.text.component.say"',
        ),
        (
            [ThreadDataEntry.get_entry_type(test_type_registry)],
            [],
            'invalid tracked entry "meya.thread.entry.data"',
        ),
        ([], ["abc"], 'invalid untracked entry "abc"'),
        (
            ["xyz"],
            ["foo", "abc"],
            "only either tracked or untracked entries is supported",
        ),
        ([UserDataEntry.get_entry_type(test_type_registry)], [], None),
        ([SayEvent.get_entry_type(test_type_registry)], [], None),
        ([ComponentStartEntry.get_entry_type(test_type_registry)], [], None),
        ([], [UserDataEntry.get_entry_type(test_type_registry)], None),
        ([], [SayEvent.get_entry_type(test_type_registry)], None),
        ([], [ComponentStartEntry.get_entry_type(test_type_registry)], None),
    ],
)
def test_validate_entry_whitelist_blacklist(
    whitelist: List[str],
    blacklist: List[str],
    validation_message: Optional[str],
):
    with TypeRegistry.current.set(test_type_registry):
        element = MockAnalyticsIntegration(
            track_entries=True,
            tracked_entries=whitelist,
            untracked_entries=blacklist,
        )
        if validation_message:
            with pytest.raises(ElementValidationError) as excinfo:
                element.validate()
            assert str(excinfo.value) == validation_message
        else:
            element.validate()


@pytest.mark.parametrize(
    ("key", "whitelist", "blacklist", "is_tracked"),
    [
        ("foo", [], [], True),
        ("foo", ["foo", "abc"], [], True),
        ("foo", ["fizz", "abc"], [], False),
        ("foo", [], ["foo", "abc"], False),
        ("foo", [], ["fizz", "abc"], True),
    ],
)
def test_user_data_whitelist_blacklist(
    key: str, whitelist: List[str], blacklist: List[str], is_tracked: bool
):
    element = MockAnalyticsIntegration(
        track_user_data=True,
        tracked_user_data=whitelist,
        untracked_user_data=blacklist,
    )
    assert element._is_user_data_key_tracked(key) == is_tracked


@pytest.mark.parametrize(
    ("entry", "whitelist", "blacklist", "is_tracked"),
    [
        (
            SayEvent(
                composer=ComposerEventSpec(),
                user_id="O123",
                quick_replies=[],
                text="T456",
                thread_id="T0",
            ),
            [],
            [],
            True,
        ),
        (
            SayEvent(
                composer=ComposerEventSpec(),
                user_id="O123",
                quick_replies=[],
                text="T456",
                thread_id="T0",
            ),
            [
                SayEvent.get_entry_type(test_type_registry),
                ComponentStartEntry.get_entry_type(test_type_registry),
            ],
            [],
            True,
        ),
        (
            SayEvent(
                composer=ComposerEventSpec(),
                user_id="O123",
                quick_replies=[],
                text="T456",
                thread_id="T0",
            ),
            [
                ComponentStartEntry.get_entry_type(test_type_registry),
                ButtonClickEvent.get_entry_type(test_type_registry),
            ],
            [],
            False,
        ),
        (
            SayEvent(
                composer=ComposerEventSpec(),
                user_id="O123",
                quick_replies=[],
                text="T456",
                thread_id="T0",
            ),
            [],
            [
                SayEvent.get_entry_type(test_type_registry),
                ComponentStartEntry.get_entry_type(test_type_registry),
            ],
            False,
        ),
        (
            SayEvent(
                composer=ComposerEventSpec(),
                user_id="O123",
                quick_replies=[],
                text="T456",
                thread_id="T0",
            ),
            [],
            [
                ComponentStartEntry.get_entry_type(test_type_registry),
                ButtonClickEvent.get_entry_type(test_type_registry),
            ],
            True,
        ),
    ],
)
def test_entry_whitelist_blacklist(
    entry: Entry, whitelist: List[str], blacklist: List[str], is_tracked: bool
):
    with TypeRegistry.current.set(test_type_registry):
        element = MockAnalyticsIntegration(
            track_entries=True,
            tracked_entries=whitelist,
            untracked_entries=blacklist,
        )
        element.redacted_entry = entry
        assert element.is_entry_tracked == is_tracked
