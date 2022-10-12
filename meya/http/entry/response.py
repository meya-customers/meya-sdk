from dataclasses import dataclass
from http import HTTPStatus
from http.cookies import SimpleCookie
from meya.entry.field import entry_field
from meya.http.entry import HttpEntry
from multidict import CIMultiDict
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple


class HttpResponseError(Exception):
    pass


class HttpUnexpectedResponseStatus(HttpResponseError):
    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        expected: Optional[Tuple[int]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.message = message
        self.status = status
        self.expected = expected
        self.data = data
        self.headers = headers

    def __str__(self):
        return f"{self.message} {self.status}. Expected {self.expected}"

    def get_header(
        self, name: str, default: Optional[str] = None
    ) -> Optional[str]:
        return CIMultiDict(self.headers or {}).get(name, default)


@dataclass
class HttpResponseEntry(HttpEntry):
    content_type: Optional[str] = entry_field()
    data: Optional[Dict[str, Any]] = entry_field(default=None, sensitive=True)
    headers: Dict[str, str] = entry_field(default_factory=dict, sensitive=True)
    status: int = entry_field()
    text: Optional[str] = entry_field(default=None, sensitive=True)
    url: Optional[str] = entry_field(default=None)

    def get_header(
        self, name: str, default: Optional[str] = None
    ) -> Optional[str]:
        return CIMultiDict(self.headers).get(name, default)

    @property
    def cookies(self) -> Dict[str, str]:
        simple_cookie = SimpleCookie(self.get_header("set-cookie", ""))
        return {key: simple_cookie[key].value for key in simple_cookie}

    def check_status(self, *expected: int):
        if self.status not in (expected or (HTTPStatus.OK,)):
            raise HttpUnexpectedResponseStatus(
                f"Unexpected response status {self.status} for request {self.request_id} at {self.url}",
                status=self.status,
                expected=expected,
                headers=self.headers,
            )
