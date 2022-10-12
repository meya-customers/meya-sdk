import pytest

from base64 import b85decode
from base64 import b85encode
from dataclasses import dataclass
from dataclasses import field
from datetime import timedelta
from meya.db.view.db import DbConfig
from meya.db.view.db import DbView
from meya.entry import Entry
from meya.event.composer_spec import ComposerEventSpec
from meya.event.header_spec import HeaderEventSpec
from meya.http.direction import Direction
from meya.http.entry.request import HttpRequestEntry
from meya.sensitive_data import REDACTED_TEXT
from meya.sensitive_data import SensitiveDataRef
from meya.text.event.say import SayEvent
from meya.util.msgpack import from_msgpack
from meya.util.msgpack import to_msgpack
from meya.zendesk.support.event.ticket.update import (
    ZendeskSupportTicketUpdateEvent,
)
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketStatus
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from unittest.mock import MagicMock


@dataclass
class MockDbConfig(DbConfig):
    @classmethod
    def __new__(cls, *args, **kwargs):
        return MagicMock()


@dataclass
class MockDbView(DbView):
    db_config: Optional[MockDbConfig] = field(
        init=False, default_factory=MockDbConfig
    )
    expected_requests: List[tuple] = field(default_factory=list)
    current_request: int = field(default=0)

    @property
    def config(self) -> Optional[MockDbConfig]:
        return self.db_config

    async def publish(
        self, *entries: Entry, preclaim_after_publish_all: bool = False
    ) -> None:
        self._check_request(list(entries))

    async def encrypt_sensitive(
        self, sensitive_obj: Any, ttl: Optional[timedelta] = None
    ) -> SensitiveDataRef:
        return SensitiveDataRef(
            ref_key_value=b85encode(to_msgpack(sensitive_obj)).decode("utf-8")
        )

    async def decrypt_sensitive(self, ref: SensitiveDataRef) -> Any:
        return from_msgpack(b85decode(ref.ref_key_value))

    async def root_entry(self, entry: Entry) -> Entry:
        return entry

    async def _query_hash_view(
        self, view: str, instance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._check_request(view, instance_data)

    async def _query_ledger(
        self,
        ledger: str,
        instance_data: Dict[str, Any],
        end: str,
        start: str,
        count: int,
    ) -> List[Any]:
        return self._check_request(ledger, instance_data, end, start, count)

    async def _query_set_view(
        self, view: str, instance_data: Dict[str, Any]
    ) -> List[Any]:
        return self._check_request(view, instance_data)

    def _check_request(self, *actual_request) -> Any:
        if self.current_request >= len(self.expected_requests):
            expected_request = ()
        else:
            expected_request = self.expected_requests[self.current_request]
        if len(expected_request) > 1:
            result = expected_request[-1]
            expected_request = expected_request[:-1]
        else:
            result = None
        assert (
            actual_request == expected_request
        ), f"DB request {self.current_request}"
        self.current_request += 1
        return result


@pytest.mark.parametrize(
    ("sensitive_entry", "expected_redacted_entry"),
    [
        (
            SayEvent(
                parent_entry_ref=None,
                trace_id="t-1",
                user_id="U0",
                sensitive=True,
                text=".",
                thread_id="T0",
                context={},
                composer=ComposerEventSpec(),
                quick_replies=[],
                header=HeaderEventSpec(),
                markdown=[],
            ),
            SayEvent(
                parent_entry_ref=None,
                trace_id="t-1",
                user_id="U0",
                sensitive=True,
                text=REDACTED_TEXT,
                thread_id="T0",
                context={},
                composer=ComposerEventSpec(),
                quick_replies=[],
                header=HeaderEventSpec(),
                markdown=[],
            ),
        ),
        (
            HttpRequestEntry(
                parent_entry_ref=None,
                trace_id="t-1",
                allow_redirects=True,
                direction=Direction.TX,
                headers={
                    "Authorization": "Basic Ym90QG1leWEuYWkvdG9rZW46dG9rZW4="
                },
                method="GET",
                params={"include": "comment_count"},
                request_id="r-~0",
                timeout=3,
                url="https://s.zendesk.com/api/v2/tickets/1.json",
            ),
            HttpRequestEntry(
                parent_entry_ref=None,
                trace_id="t-1",
                allow_redirects=True,
                direction=Direction.TX,
                headers={REDACTED_TEXT: REDACTED_TEXT},
                method="GET",
                params={REDACTED_TEXT: REDACTED_TEXT},
                request_id="r-~0",
                timeout=3,
                url="https://s.zendesk.com/api/v2/tickets/1.json",
            ),
        ),
        (
            ZendeskSupportTicketUpdateEvent(
                parent_entry_ref=None,
                trace_id="t-1",
                sensitive=True,
                user_id="u-7d1e808bda6e420085b1aa3473218024",
                thread_id="t-06e20ccb673e4e3faed1129bf92a4604",
                integration_id="z1",
                context={},
                old_ticket=ZendeskSupportTicketGet(
                    assignee_id=None,
                    custom_fields=[],
                    external_id=None,
                    group_id=None,
                    priority=None,
                    requester_id=416025657633,
                    status=ZendeskSupportTicketStatus.NEW,
                    subject="⭑⭑⭑⭑⭑⭑",
                    tags=[],
                    type=None,
                    created_at="2020-07-15T19:32:50Z",
                    description="⭑⭑⭑⭑⭑⭑",
                    id=1519,
                    updated_at="2020-07-15T19:32:50Z",
                    comment_count=2,
                ),
                ticket=ZendeskSupportTicketGet(
                    assignee_id=None,
                    custom_fields=[],
                    external_id=None,
                    group_id=None,
                    priority=None,
                    requester_id=416025657633,
                    status=ZendeskSupportTicketStatus.NEW,
                    subject="⭑⭑⭑⭑⭑⭑",
                    tags=[],
                    type=None,
                    created_at="2020-07-15T19:32:50Z",
                    description="⭑⭑⭑⭑⭑⭑",
                    id=1519,
                    updated_at="2020-07-15T19:32:50Z",
                    comment_count=3,
                ),
            ),
            ZendeskSupportTicketUpdateEvent(
                parent_entry_ref=None,
                trace_id="t-1",
                sensitive=True,
                user_id="u-7d1e808bda6e420085b1aa3473218024",
                thread_id="t-06e20ccb673e4e3faed1129bf92a4604",
                integration_id="z1",
                context={},
                old_ticket=REDACTED_TEXT,
                ticket=REDACTED_TEXT,
            ),
        ),
    ],
)
def test_redact_sensitve_entry(
    sensitive_entry: Entry, expected_redacted_entry: Entry
):
    from meya.element.element_test import test_type_registry

    db_view = MockDbView()
    actual_redacted_entry = db_view.redact_sensitive_entry(sensitive_entry)
    assert actual_redacted_entry == expected_redacted_entry
    assert (
        Entry.from_typed_dict(
            actual_redacted_entry.to_typed_dict(test_type_registry),
            test_type_registry,
        )
        == expected_redacted_entry
    )
