from dataclasses import dataclass
from dataclasses import field
from meya.db.view.db import DbView
from meya.db.view.db_test import MockDbView
from meya.db.view.http import HttpBasicAuth
from meya.db.view.http import HttpView
from meya.http.direction import Direction
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.util.uuid_test import patch_uuid4_hex
from typing import List
from typing import Optional


@dataclass
class MockHttpView(HttpView):
    db_view: DbView = field(default_factory=MockDbView)
    expected_requests: Optional[List[HttpRequestEntry]] = field(default=None)
    expected_responses: List[HttpResponseEntry] = field(default_factory=list)
    current_request: int = field(default=0)

    async def _send(self, req: HttpRequestEntry) -> HttpResponseEntry:
        if self.current_request >= (
            min(len(self.expected_requests), len(self.expected_responses))
            if self.expected_requests is not None
            else len(self.expected_responses)
        ):
            assert req is None, f"request {self.current_request}"
        if self.expected_requests is not None:
            expected_request = self.expected_requests[self.current_request]
            assert expected_request == req, f"request {self.current_request}"
        response = self.expected_responses[self.current_request]
        self.current_request += 1
        return response


def test_http_basic_auth():
    test_header = {"Authorization": "Basic dGVzdDp0ZXN0X3Bhc3N3b3Jk"}

    auth = HttpBasicAuth("test", "test_password")
    assert auth({}) == test_header


@patch_uuid4_hex()
def test_request_entry_full_data():
    test_auth_header = {"Authorization": "Basic dGVzdDp0ZXN0X3Bhc3N3b3Jk"}
    test_auth = HttpBasicAuth("test", "test_password")

    test_entry = HttpRequestEntry(
        allow_redirects=True,
        app_id="A1234",
        content_type=None,
        cookies={"cookie1": "choc chip"},
        data={"test": "data"},
        headers={"Token": "1234"},
        integration_name="test",
        integration_id="I1234",
        method="GET",
        direction=Direction.TX,
        params={"a": "b", "c": "d"},
        request_id="r-~0",
        text=None,
        timeout=10.4,
        url="https://test.com",
    )

    entry = MockHttpView().make_request_entry(
        test_entry.method,
        test_entry.url,
        allow_redirects=test_entry.allow_redirects,
        app_id=test_entry.app_id,
        auth=test_auth,
        cookies=test_entry.cookies,
        data=test_entry.data,
        headers=test_entry.headers,
        integration_name=test_entry.integration_name,
        integration_id=test_entry.integration_id,
        params=test_entry.params,
        timeout=test_entry.timeout,
    )

    test_entry.headers.update(test_auth_header)

    assert entry == test_entry


@patch_uuid4_hex()
def test_request_entry_bare_data():
    test_entry = HttpRequestEntry(
        allow_redirects=True,
        app_id=None,
        content_type=None,
        cookies={},
        data=None,
        headers={},
        integration_name=None,
        integration_id=None,
        method="GET",
        direction=Direction.TX,
        params={},
        request_id="r-~0",
        text=None,
        timeout=3.0,
        url="https://test.com",
    )

    entry = MockHttpView().make_request_entry(
        test_entry.method, test_entry.url
    )

    assert entry == test_entry


@patch_uuid4_hex()
def test_request_entry_empty_data():
    test_entry = HttpRequestEntry(
        allow_redirects=True,
        app_id=None,
        content_type=None,
        cookies={},
        data=None,
        headers={},
        integration_name=None,
        integration_id=None,
        method="GET",
        direction=Direction.TX,
        params={},
        request_id="r-~0",
        text=None,
        timeout=3.0,
        url="https://test.com",
    )

    entry = MockHttpView().make_request_entry(
        test_entry.method,
        test_entry.url,
        cookies={},
        data=None,
        headers={},
        params={},
    )

    assert entry == test_entry
