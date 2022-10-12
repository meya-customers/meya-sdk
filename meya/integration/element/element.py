from dataclasses import MISSING
from dataclasses import dataclass
from http import HTTPStatus
from meya import env
from meya.core.abstract_type_registry import AbstractTypeRegistry
from meya.core.type_registry import TypeRegistry
from meya.db.view.http import AuthBase
from meya.db.view.thread import ThreadMode
from meya.db.view.user import UserType
from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event.entry import Event
from meya.gridql.parser import GridQL
from meya.gridql.parser import QueryException
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.icon.spec import IconElementSpecUnion
from meya.lifecycle.event.event import LifecycleEvent
from meya.media.event import MediaEvent
from meya.util.context_var import ScopedContextVar
from meya.util.dict import to_dict
from os import path
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import cast

FilterElementSpecUnion = Union[bool, str]

EntryFilterElementSpecUnion = FilterElementSpecUnion  # Backwards compatibility


@dataclass
class IntegrationFilter:
    rx_sub: FilterElementSpecUnion = element_field(default=True)
    rx: FilterElementSpecUnion = element_field(default=True)
    tx: FilterElementSpecUnion = element_field(default=True)
    tx_pub: FilterElementSpecUnion = element_field(default=True)

    def is_valid(self) -> (bool, Optional[str]):
        """
        :return: True, None if valid, False, "error message" otherwise
        """
        tests = (
            ("rx_sub", self.rx_sub),
            ("rx", self.rx),
            ("tx", self.tx),
            ("tx_pub", self.tx_pub),
        )
        for name, value in tests:
            if not isinstance(value, bool):
                try:
                    # try parse and match to validate the input
                    gridql = GridQL.create(
                        value, type_registry=TypeRegistry.current.get()
                    )
                    gridql.match_entry(Event())
                except QueryException as e:
                    return (
                        False,
                        f"Invalid GridQL for `{name}` field with value `{value}`: {str(e)}",
                    )
        return True, None

    @staticmethod
    def does_match(entry: Entry, field: FilterElementSpecUnion) -> bool:
        """
        :return: true|false whether or not to continue processing
        """
        if isinstance(field, bool):
            return field
        else:
            # Lucene style match
            return GridQL.create(
                field, type_registry=AbstractTypeRegistry.current.get()
            ).match_entry(entry)

    @staticmethod
    def filter_matches(
        entries: List[Entry], field: FilterElementSpecUnion
    ) -> List[Entry]:
        """
        :return: list of entries matching a given filter
        """
        if isinstance(field, bool):
            return entries
        else:
            gridsql = GridQL.create(
                field, type_registry=AbstractTypeRegistry.current.get()
            )
            return [entry for entry in entries if gridsql.match_entry(entry)]


@dataclass
class Integration(Element):
    NAME: ClassVar[str] = "generic"

    current: ClassVar = cast(
        ScopedContextVar["AbstractTypeRegistry"], ScopedContextVar()
    )
    allowed_methods: ClassVar[Tuple[str]] = ("GET", "POST")
    show_get_status: ClassVar[bool] = True

    is_abstract: bool = meta_field(value=True)
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/05-internet-networks-servers/09-cloud/cloud-settings.svg"
    )

    entry: Union[HttpRequestEntry, Event] = process_field()
    request: Optional[HttpRequestEntry] = process_field()
    event: Optional[Event] = process_field()
    suppress_echo: bool = process_field(default=True)

    enabled: bool = element_field(
        default=True,
        help="Enables the integration, allowing it to process events and HTTP entries",
    )
    filter: IntegrationFilter = element_field(
        default_factory=IntegrationFilter
    )
    verify_token: Optional[str] = element_field(default=None)
    max_attachment_size: Optional[int] = element_field(
        default=None,
        help="Controls maximum attachment size supported by the integration in bytes",
    )

    @dataclass
    class RxResponse:
        ok: bool = response_field()
        accepted: bool = response_field()
        message: Optional[str] = response_field()
        error: str = response_field(default=None)
        result: Any = response_field(default=None)

    def __post_init__(self):
        super().__post_init__()
        self.request = (
            self.entry if isinstance(self.entry, HttpRequestEntry) else None
        )
        self.event = self.entry if isinstance(self.entry, Event) else None

    def validate(self):
        super().validate()

        # only do design-time checks on GridQL filter
        if self.is_design_time:
            valid, error = self.filter.is_valid()
            if not valid:
                raise self.validation_error(error)

    async def accept(self) -> bool:
        if not await super().accept():
            return False
        elif not self.enabled:
            return False
        elif self.request:
            return self.request.integration_id == self.id
        else:
            return True

    async def accept_sensitive(self) -> bool:
        if isinstance(self.entry, HttpRequestEntry):
            return await self.accept()
        else:
            return False

    async def process(self) -> List[Entry]:
        with self.current.set(self):
            if self.is_rx:
                # allowed methods
                if self.request:
                    if self.request.method not in self.allowed_methods:
                        return self.respond(
                            status=HTTPStatus.METHOD_NOT_ALLOWED,
                            data=self.RxResponse(
                                ok=False,
                                accepted=False,
                                message=f"Only {self.allowed_methods} methods allowed.",
                            ),
                        )

                # auth
                auth_entries = await self.check_rx_auth()
                if auth_entries:
                    return auth_entries
                # Validate verify token
                verify_token_entries = await self.check_rx_verify_token()
                if verify_token_entries:
                    return verify_token_entries
                # rx_sub filter
                if not IntegrationFilter.does_match(
                    self.entry, self.filter.rx_sub
                ):
                    return self.quick_return(
                        message="Payload filtered by integration GridQL"
                    )

                # GET response
                if (
                    self.show_get_status
                    and self.request
                    and self.request.method == "GET"
                ):
                    pub_entries = await self.rx_get()
                else:
                    pub_entries = await self.rx()

                # rx_pub filter
                return IntegrationFilter.filter_matches(
                    pub_entries, self.filter.rx
                )

            elif self.is_tx:
                # echo suppression
                if self.is_echo_suppressed:
                    return self.quick_return()

                # tx_sub filter
                if not IntegrationFilter.does_match(
                    self.entry, self.filter.tx
                ):
                    return self.quick_return()

                # tx_pub filter
                return IntegrationFilter.filter_matches(
                    await self.tx(), self.filter.tx_pub
                )

            else:
                raise NotImplementedError()

    @property
    def is_rx(self) -> bool:
        return bool(self.request)

    @property
    def is_tx(self) -> bool:
        return bool(self.event)

    def quick_return(self, message: Optional[str] = None) -> List[Entry]:
        if bool(self.request):
            return self.respond(
                status=HTTPStatus.OK,
                data=self.RxResponse(ok=True, accepted=False, message=message),
            )
        else:
            return []

    @property
    def is_echo_suppressed(self) -> bool:
        if self.is_tx:
            return self.suppress_echo and self.event.integration_id == self.id
        else:
            return False

    async def check_rx_verify_token(self) -> List[Entry]:
        if self.verify_token:
            if not self.request.params.get("verify_token"):
                return self.respond(
                    status=HTTPStatus.UNAUTHORIZED,
                    data=self.RxResponse(
                        ok=False,
                        accepted=False,
                        error="Verify token is missing.",
                    ),
                )

            if self.request.params.get("verify_token") != self.verify_token:
                return self.respond(
                    status=HTTPStatus.FORBIDDEN,
                    data=self.RxResponse(
                        ok=False,
                        accepted=False,
                        error="Verify token is invalid.",
                    ),
                )

        return []

    async def check_rx_auth(self) -> List[Entry]:
        expected = self.rx_auth
        if not expected:
            return []

        actual = self.request.get_header("Authorization")
        if not actual:
            return self.respond(
                status=HTTPStatus.UNAUTHORIZED,
                data=self.RxResponse(
                    ok=False,
                    accepted=False,
                    error="Authentication credentials were not provided.",
                ),
            )
        if isinstance(expected, AuthBase):
            expected = cast(dict, expected({}))["Authorization"]
        if actual != expected:
            return self.respond(
                status=HTTPStatus.FORBIDDEN,
                data=self.RxResponse(
                    ok=False, accepted=False, error="Invalid api_key."
                ),
            )
        return []

    @property
    def rx_auth(self) -> Optional[Union[AuthBase, str]]:
        return None

    async def rx(self) -> List[Entry]:
        return self.quick_return()

    async def rx_get(self) -> List[Entry]:
        return self.respond(
            status=HTTPStatus.OK,
            data=self.RxResponse(
                ok=True, accepted=False, message=f"Valid `{self.NAME}` webhook"
            ),
        )

    async def tx(self) -> List[Entry]:
        return self.quick_return()

    def post_process(self, entry: Entry, extra_entries: List[Entry]) -> None:
        super().post_process(entry, extra_entries)

        if isinstance(entry, Event):
            event_user = None

            if entry.user_id is MISSING and self.event_user.id:
                entry.user_id = self.event_user.id
                event_user = self.event_user

            if entry.user_id is MISSING and self.user.id:
                # TODO Remove deprecated self.user.id integration RX
                self.log.warning(
                    "Switch to self.event_user instead of self.user for integration RX"
                )
                entry.user_id = self.user.id
                event_user = self.user

            thread = None

            if entry.thread_id is MISSING and self.thread.id:
                entry.thread_id = self.thread.id
                thread = self.thread

            if entry.integration_id is MISSING and self.id:
                entry.integration_id = self.id

            if entry.context is MISSING:
                entry.context = {}

            if not entry.sensitive and event_user and thread:
                if event_user.type == UserType.USER:
                    if (
                        isinstance(entry, (MediaEvent, LifecycleEvent))
                        or thread.mode != ThreadMode.BOT
                    ):
                        entry.sensitive = True
                elif event_user.type == UserType.AGENT:
                    entry.sensitive = True
                elif event_user.type == UserType.SYSTEM:
                    entry.sensitive = True

    @classmethod
    def get_gateway_webhook_url(cls, integration_id: str, app_id: str) -> str:
        return path.join(
            env.grid_url, "gateway", "v2", cls.NAME, app_id, integration_id
        )

    @property
    def gateway_webhook_url(self) -> str:
        return self.get_gateway_webhook_url(
            app_id=env.app_id, integration_id=self.id
        )

    def respond(
        self,
        *entries: Entry,
        status: int,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = "application/json",
        text: Optional[str] = None,
    ) -> List[Entry]:
        return [
            *entries,
            self.create_response(
                self.request.request_id,
                status,
                to_dict(data, preserve_nones=False),
                headers,
                self.request.url,
                content_type,
                text,
            ),
        ]

    @staticmethod
    def create_response(
        request_id: str,
        status: int,
        data: Optional[dict] = None,
        headers: Optional[Dict[str, str]] = None,
        url: Optional[str] = None,
        content_type: Optional[str] = "application/json",
        text: Optional[str] = None,
    ):
        if data is None:
            data = {"ok": True}
        return HttpResponseEntry(
            content_type=content_type,
            data=data,
            text=text,
            url=url,
            headers=headers or {},
            request_id=request_id,
            status=status,
        )


class IntegrationSpec(Spec):
    element_type: ClassVar[Type[Element]] = Integration


class IntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = Integration
