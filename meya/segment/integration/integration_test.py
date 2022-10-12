import pytest

from meya.analytics.event.identify import IdentifyEvent
from meya.analytics.event.track import TrackEvent
from meya.element.element_test import create_user
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_process_element
from meya.entry import Entry
from meya.event.composer_spec import ComposerEventSpec
from meya.event.header_spec import HeaderEventSpec
from meya.flow.entry.start import FlowStartEntry
from meya.http.direction import Direction
from meya.http.entry.request import HttpRequestEntry
from meya.segment.integration import SegmentIntegration
from meya.segment.integration.api import timestamp_to_ISO8601
from meya.text.event.say import SayEvent
from meya.user.entry.data import UserDataEntry
from typing import Any
from typing import List
from typing import Optional

WRITE_KEY = "SEGMENT_WRITE_KEY-123"

FLOW_START_ENTRY = FlowStartEntry(
    bot_id="segment_bot",
    data=dict(foo="bar", pi=3.14159),
    flow="test_flow_abc",
    label=None,
    stack=[],
    thread_id="t-0",
    trace_id="-",
)


def _create_tx_request_entry(
    request_data: dict, method: str
) -> HttpRequestEntry:
    return HttpRequestEntry(
        allow_redirects=True,
        app_id=None,
        content_type="application/json",
        cookies={},
        data=request_data,
        headers={"Authorization": "Basic U0VHTUVOVF9XUklURV9LRVktMTIzOg=="},
        integration_name=None,
        integration_id=None,
        method="POST",
        direction=Direction.TX,
        params={},
        request_id="r-~0",
        text=None,
        timeout=3.0,
        url=f"https://api.segment.io/v1/{method}",
    )


@pytest.mark.parametrize(
    ("sub_entry", "tracked_entries", "untracked_entries", "is_tracked"),
    [
        (FLOW_START_ENTRY, [], [], True),
        (
            FLOW_START_ENTRY,
            [
                FlowStartEntry.get_entry_type(test_type_registry),
                SayEvent.get_entry_type(test_type_registry),
            ],
            [],
            True,
        ),
        (
            FLOW_START_ENTRY,
            [],
            [
                FlowStartEntry.get_entry_type(test_type_registry),
                SayEvent.get_entry_type(test_type_registry),
            ],
            False,
        ),
        (UserDataEntry(user_id="U123", key="foo", value="bar"), [], [], False),
    ],
)
@pytest.mark.asyncio
async def test_segment_track_entry(
    sub_entry: Entry,
    tracked_entries: List[str],
    untracked_entries: List[str],
    is_tracked: bool,
):
    sub_entry.entry_id = "1569945588469-0"
    integration = SegmentIntegration(
        write_key=WRITE_KEY,
        tracked_entries=tracked_entries,
        untracked_entries=untracked_entries,
        track_user_data=False,
    )
    user = create_user()
    if is_tracked:
        request_entry = _create_tx_request_entry(
            {
                "event": sub_entry.get_entry_type(test_type_registry),
                "userId": user.id,
                "properties": sub_entry.to_dict(),
                "timestamp": timestamp_to_ISO8601(
                    sub_entry.entry_posix_timestamp
                ),
            },
            "track",
        )
        pub_entries = [request_entry]
    else:
        pub_entries = []

    await verify_process_element(
        element=integration,
        sub_entry=sub_entry,
        expected_pub_entries=pub_entries,
        user=user,
    )


@pytest.mark.asyncio
async def test_segment_track_redacted():
    sub_entry = SayEvent(
        composer=ComposerEventSpec(),
        context={"hidden": True},
        integration_id="I123",
        markdown=[],
        quick_replies=[],
        header=HeaderEventSpec(),
        sensitive=True,
        text="HI",
        thread_id="T123",
        user_id="U123",
    )
    sub_entry.entry_id = "1569945588469-0"
    integration = SegmentIntegration(
        write_key=WRITE_KEY,
        tracked_entries=[SayEvent.get_entry_type(test_type_registry)],
        untracked_entries=[],
        track_user_data=False,
    )
    user = create_user()
    await verify_process_element(
        element=integration,
        sub_entry=sub_entry,
        expected_pub_entries=[
            _create_tx_request_entry(
                {
                    "event": sub_entry.get_entry_type(test_type_registry),
                    "userId": user.id,
                    "properties": {
                        "trace_id": "-",
                        "sensitive": True,
                        "user_id": "U123",
                        "thread_id": "T123",
                        "integration_id": "I123",
                        "context": {},
                        "composer": {},
                        "header": {},
                        "quick_replies": [],
                        "markdown": [],
                        "text": "⭑⭑⭑⭑⭑⭑",
                    },
                    "timestamp": timestamp_to_ISO8601(
                        sub_entry.entry_posix_timestamp
                    ),
                    "context": {},
                },
                "track",
            )
        ],
        user=user,
    )


@pytest.mark.parametrize(
    ("track", "data", "context", "timestamp"),
    [
        ("custom_event_abc", None, {}, None),
        ("custom_event_123", dict(pi=3.14159, foo="bar"), {}, None),
        (
            "custom_event_DEF",
            dict(pi=3.14159, foo="bar"),
            dict(ip="127.0.0.1"),
            None,
        ),
        (
            "custom_event_456",
            dict(pi=3.14159, foo="bar"),
            dict(ip="127.0.0.1"),
            1569957070.488,
        ),
    ],
)
@pytest.mark.asyncio
async def test_segment_track_event(
    track: str, data: Optional[dict], context: dict, timestamp: Optional[float]
):
    integration = SegmentIntegration(write_key=WRITE_KEY)
    user = create_user()
    track_event = TrackEvent(
        user_id=user.id,
        thread_id="t-0",
        event=track,
        data=data,
        context=context,
        timestamp=timestamp,
    )
    track_event.entry_id = "1569945588469-0"
    request_data = {
        "event": track,
        "userId": user.id,
        "timestamp": timestamp_to_ISO8601(
            track_event.timestamp or track_event.entry_posix_timestamp
        ),
    }
    if data is not None:
        request_data["properties"] = data
    if context is not None:
        request_data["context"] = context
    await verify_process_element(
        element=integration,
        sub_entry=track_event,
        expected_pub_entries=[_create_tx_request_entry(request_data, "track")],
        user=user,
    )


@pytest.mark.parametrize(
    ("key", "value", "tracked_user_data", "untracked_user_data", "is_tracked"),
    [
        ("foo", "bar", ["foo", "abc"], [], True),
        ("age", 40, [], ["SIN", "CC", "DOB"], True),
        ("SIN", "xxxxyyyyy", [], ["SIN", "CC", "DOB"], False),
        ("pi", 3.14159, [], [], True),
        ("name", dict(name="Greta", age=16), [], [], True),
    ],
)
@pytest.mark.asyncio
async def test_segment_identify(
    key: str,
    value: Any,
    tracked_user_data: List[str],
    untracked_user_data: List[str],
    is_tracked: bool,
):
    integration = SegmentIntegration(
        write_key=WRITE_KEY,
        tracked_user_data=tracked_user_data,
        untracked_user_data=untracked_user_data,
    )
    user_id = "U123"
    user = create_user()
    sub_entry = UserDataEntry(user_id=user_id, key=key, value=value)
    sub_entry.entry_id = "1569945588469-0"
    if is_tracked:
        request_entry = _create_tx_request_entry(
            {
                "userId": sub_entry.user_id,
                "traits": {key: value},
                "timestamp": timestamp_to_ISO8601(
                    sub_entry.entry_posix_timestamp
                ),
            },
            "identify",
        )
        pub_entries = [request_entry]
    else:
        pub_entries = []

    await verify_process_element(
        element=integration,
        sub_entry=sub_entry,
        expected_pub_entries=pub_entries,
        user=user,
    )


@pytest.mark.parametrize(
    (
        "identify",
        "context",
        "timestamp",
        "tracked_user_data",
        "untracked_user_data",
    ),
    [
        (dict(pi=3.141, foo="bar"), {}, None, None, None),
        (dict(pi=3.141, foo="bar"), dict(ip="127.0.0.1"), None, None, None),
        (
            dict(pi=3.141, foo="bar"),
            dict(ip="127.0.0.1"),
            1569957070.488,
            None,
            None,
        ),
        (
            dict(pi=3.141, foo="bar", private="SECRET"),
            {},
            None,
            ["pi", "foo"],
            None,
        ),
        (
            dict(pi=3.141, foo="bar", private="SECRET"),
            {},
            None,
            None,
            ["private"],
        ),
        (
            dict(pi=3.141, foo="bar", private="SECRET"),
            {},
            None,
            ["A", "B"],
            None,
        ),
        (
            dict(pi=3.141, foo="bar", private="SECRET"),
            {},
            None,
            None,
            ["pi", "foo", "private", "A", "B"],
        ),
    ],
)
@pytest.mark.asyncio
async def test_segment_identify_event(
    identify: dict,
    context: dict,
    timestamp: Optional[float],
    tracked_user_data: Optional[List[str]],
    untracked_user_data: Optional[List[str]],
):
    tracked_user_data = tracked_user_data or []
    untracked_user_data = untracked_user_data or []
    integration = SegmentIntegration(
        write_key=WRITE_KEY,
        tracked_user_data=tracked_user_data,
        untracked_user_data=untracked_user_data,
    )
    user = create_user()
    if tracked_user_data:
        data = {
            key: identify[key] for key in tracked_user_data if key in identify
        }
        assert set(data.keys()).issubset(set(tracked_user_data))
    elif untracked_user_data:
        data = {
            key: identify[key]
            for key in identify
            if key not in untracked_user_data
        }
        assert set(data.keys()).isdisjoint(set(untracked_user_data))
    else:
        data = identify
    identify_event = IdentifyEvent(
        user_id=user.id,
        thread_id="t-0",
        data=identify,
        context=context,
        timestamp=timestamp,
    )
    identify_event.entry_id = "1569945588469-0"
    request_data = {
        "userId": user.id,
        "traits": data,
        "timestamp": timestamp_to_ISO8601(
            identify_event.timestamp or identify_event.entry_posix_timestamp
        ),
    }
    if context is not None:
        request_data["context"] = context
    if data:
        pub_entries = [_create_tx_request_entry(request_data, "identify")]
    else:
        pub_entries = []
    await verify_process_element(
        element=integration,
        sub_entry=identify_event,
        expected_pub_entries=pub_entries,
        user=user,
    )


@pytest.mark.parametrize(
    ("timestamp", "iso8601"),
    [
        (1569945588.469, "2019-10-01T15:59:48.469000Z"),
        (1569945588, "2019-10-01T15:59:48Z"),
        (1577854800.0, "2020-01-01T05:00:00Z"),
    ],
)
def test_timestamp_to_ISO8601(timestamp: float, iso8601: str):
    assert timestamp_to_ISO8601(timestamp) == iso8601
