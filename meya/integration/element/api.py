from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from http import HTTPStatus
from meya.db.view.http import HttpView
from meya.db.view.log import LogView
from meya.element.field import response_field


class ApiError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

    def __str__(self):
        return f"{self.status}: {self.message}"


@dataclass
class ApiComponentResponse:
    result: dict = response_field(sensitive=True)
    status: int = response_field()
    ok: bool = response_field()

    @classmethod
    def create_timeout(cls) -> "ApiComponentResponse":
        return cls(
            result={"error": "An HTTP timeout occurred."},
            status=HTTPStatus.GATEWAY_TIMEOUT,
            ok=False,
        )


@dataclass
class Api(ABC):
    http: HttpView = field(init=False)
    log: LogView = field(init=False)

    def __post_init__(self):
        self.http = HttpView.current.get()
        self.log = LogView.current.get()
