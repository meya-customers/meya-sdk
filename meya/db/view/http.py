import asyncio

from abc import abstractmethod
from base64 import b64decode
from base64 import b64encode
from dataclasses import dataclass
from meya.db.view.db import DbView
from meya.http.direction import Direction
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.util.context_var import ScopedContextVar
from meya.util.generate_id import generate_request_id
from numbers import Real
from typing import ClassVar
from typing import Optional
from typing import cast

DEFAULT_TIMEOUT = 3.0


class AuthBase(object):
    def __call__(self, r):
        raise NotImplementedError("Auth hooks must be callable.")


class HttpBasicAuth(AuthBase):
    """
    Attaches HTTP Basic Authentication to the headers of the
    :class:`MeyaRequestHttpEntry`
    """

    def __init__(self, username: str, password: str):
        self.username = username.encode("latin1")
        self.password = password.encode("latin1")

    def __eq__(self, other):
        return all(
            [
                self.username == getattr(other, "username", None),
                self.password == getattr(other, "password", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, headers):
        headers["Authorization"] = "Basic " + b64encode(
            b":".join((self.username, self.password))
        ).strip().decode("latin1")
        return headers

    @classmethod
    def create(cls, headers: dict) -> Optional["HttpBasicAuth"]:
        """
        :param headers: A dictionary of http headers
        :return:
        - `HttpBasicAuth` initialized w/ username, password
        - `None` if there is an error reading, parsing or decoding
        """
        try:
            authorization = headers["Authorization"]
            if not (authorization or "").startswith("Basic "):
                raise ValueError
            basic_auth = authorization.split("Basic ")[1]
            # decode and split username:password, pass as args to constructor
            return cls(*b64decode(basic_auth).decode().split(":", 1))
        except (IndexError, KeyError, UnicodeDecodeError, ValueError):
            return None


class HttpError(Exception):
    pass


class HttpTimeoutError(HttpError):
    pass


class HttpClientConnectorError(HttpError):
    pass


class HttpInvalidURL(HttpError):
    pass


class HttpClientOSError(HttpError):
    pass


class TokenAuth(AuthBase):
    """
    Attaches Token Authentication to the headers of the
    :class:`MeyaRequestHttpEntry`
    """

    def __init__(self, token: str):
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, "token", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, headers):
        headers["Authorization"] = f"{self.type} {self.token}"
        return headers

    @property
    def type(self) -> str:
        return "Token"


class BearerAuth(TokenAuth):
    @property
    def type(self) -> str:
        return "Bearer"


@dataclass
class HttpView:
    current: ClassVar = cast(ScopedContextVar["HttpView"], ScopedContextVar())

    db_view: DbView

    def make_request_entry(
        self,
        method: str,
        url: str,
        *,
        allow_redirects: bool = True,
        app_id: Optional[str] = None,
        auth: Optional[AuthBase] = None,
        content_type: Optional[str] = None,
        cookies: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        integration_name: Optional[str] = None,
        integration_id: Optional[str] = None,
        json: Optional[dict] = None,
        direction: Direction = Direction.TX,
        params: Optional[dict] = None,
        request_id: Optional[str] = None,
        text: Optional[str] = None,
        timeout: Real = DEFAULT_TIMEOUT,
        internal: bool = False,
    ) -> HttpRequestEntry:
        """
        :param method: method for the new :class:`MeyaRequestHttpEntry` object.
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the body of the :class:`MeyaRequestHttpEntry`.
        :param data: (optional) Dictionary to send in the body of the
               :class:`MeyaRequestHttpEntry`.
        :param json: (optional) A JSON serializable Python object to send in the
               body of the :class:`MeyaRequestHttpEntry`.
        :param text: (optional) A text string to send in the body of the
               :class:`MeyaRequestHttpEntry`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
               :class:`MeyaRequestHttpEntry`.
        :param auth: (optional) Auth object that defines the authentication headers.
        :type auth: AuthBase
        :param cookies: (optional) Dictionary of cookies to be added to the
               header.
        :type timeout: float
        :param allow_redirects: (optional) Boolean. Enable/disable
               GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to
               ``True``.
        :type allow_redirects: bool
        :param app_id: (optional) The ID of the grid application making this
               request.
        :param integration_id: (optional) The ID of the specific integration making
               this request.
        :param internal: Mark this request as an internal request. Defaults to `False`.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """
        if json:
            data = json
            content_type = "application/json"

        if auth and isinstance(auth, AuthBase):
            headers = auth(headers or {})

        if not request_id:
            request_id = generate_request_id()

        return HttpRequestEntry(
            allow_redirects=allow_redirects,
            app_id=app_id,
            content_type=content_type,
            cookies=cookies or {},
            data=data,
            headers=headers or {},
            integration_name=integration_name,
            integration_id=integration_id,
            method=method,
            direction=direction,
            params=params or {},
            request_id=request_id,
            text=text,
            timeout=timeout,
            url=url,
            internal=internal,
        )

    async def request(
        self, method: str, url: str, **kwargs
    ) -> HttpResponseEntry:
        """
        Usage::
          response = await self.http.request('GET', 'https://httpbin.org/get')
          <MeyaResponseHttpEntry [200]>
        """
        return await self.send(self.make_request_entry(method, url, **kwargs))

    async def send(self, request: HttpRequestEntry) -> HttpResponseEntry:
        try:
            if (
                request.sensitive
                and not self.db_view.config.http_ledger.sensitive_ttl
            ):
                request.sensitive = False
            return await self._send(request)
        except Exception as e:
            import aiohttp

            if isinstance(e, asyncio.TimeoutError):
                # TODO: in the app use-case, all error appear as TimeoutError
                raise HttpTimeoutError(e)
            elif isinstance(e, aiohttp.ClientConnectorError):
                raise HttpClientConnectorError(e)
            elif isinstance(e, aiohttp.InvalidURL):
                raise HttpInvalidURL(e)
            elif isinstance(e, aiohttp.ClientOSError):
                raise HttpClientOSError(e)
            else:
                raise HttpError(e)

    async def get(self, url: str, params=None, **kwargs) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the body of the :class:`MeyaRequestHttpEntry`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        kwargs.setdefault("allow_redirects", True)
        return await self.request("GET", url, params=params, **kwargs)

    async def options(self, url: str, **kwargs) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        kwargs.setdefault("allow_redirects", True)
        return await self.request("OPTIONS", url, **kwargs)

    async def head(self, url: str, **kwargs) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        kwargs.setdefault("allow_redirects", False)
        return await self.request("HEAD", url, **kwargs)

    async def post(
        self, url: str, data=None, json=None, **kwargs
    ) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param data: (optional) Dictionary to send in the body of the :class:`MeyaRequestHttpEntry`.
        :param json: (optional) json data to send in the body of the :class:`MeyaRequestHttpEntry`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        return await self.request("POST", url, data=data, json=json, **kwargs)

    async def put(self, url: str, data=None, **kwargs) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param data: (optional) Dictionary to send in the body of the :class:`MeyaRequestHttpEntry`.
        :param json: (optional) json data to send in the body of the :class:`MeyaRequestHttpEntry`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        return await self.request("PUT", url, data=data, **kwargs)

    async def patch(self, url: str, data=None, **kwargs) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param data: (optional) Dictionary to send in the body of the :class:`MeyaRequestHttpEntry`.
        :param json: (optional) json data to send in the body of the :class:`MeyaRequestHttpEntry`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        return await self.request("PATCH", url, data=data, **kwargs)

    async def delete(self, url: str, **kwargs) -> HttpResponseEntry:
        r"""
        :param url: URL for the new :class:`MeyaRequestHttpEntry` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`MeyaResponseHttpEntry <MeyaResponseHttpEntry>` object
        :rtype: http.MeyaResponseHttpEntry
        """

        return await self.request("DELETE", url, **kwargs)

    @abstractmethod
    async def _send(self, req: HttpRequestEntry) -> HttpResponseEntry:
        pass

    async def find_request(
        self, request_id: str
    ) -> Optional[HttpRequestEntry]:
        """
        Try to find the decrypted request entry for a given request ID.
        """
        request = await self.find_encrypted_request(request_id)
        return request and await self.db_view.try_decrypt_sensitive_entry(
            request
        )

    async def find_encrypted_request(
        self, request_id: str
    ) -> Optional[HttpRequestEntry]:
        """
        Try to find the encrypted request entry for a given request ID.
        """
        return next(
            (
                http_entry
                for http_entry in await self.db_view.query_http_ledger(
                    request_id
                )
                if isinstance(http_entry, HttpRequestEntry)
            ),
            None,
        )

    async def find_redacted_request(
        self, request_id: str
    ) -> Optional[HttpRequestEntry]:
        """
        Try to find the redacted request entry for a given request ID.
        """
        request = await self.find_encrypted_request(request_id)
        return request and self.db_view.redact_sensitive_entry(request)

    async def find_response(
        self, request_id: str
    ) -> Optional[HttpResponseEntry]:
        """
        Try to find the decrypted response entry for a given request ID.
        """
        response = await self.find_encrypted_response(request_id)
        return response and await self.db_view.try_decrypt_sensitive_entry(
            response
        )

    async def find_encrypted_response(
        self, request_id: str
    ) -> Optional[HttpResponseEntry]:
        """
        Try to find the encrypted response entry for a given request ID.
        """
        return next(
            (
                http_entry
                for http_entry in await self.db_view.query_http_ledger(
                    request_id
                )
                if isinstance(http_entry, HttpResponseEntry)
            ),
            None,
        )

    async def find_redacted_response(
        self, request_id: str
    ) -> Optional[HttpResponseEntry]:
        """
        Try to find the redacted response entry for a given request ID.
        """
        response = await self.find_encrypted_response(request_id)
        return response and self.db_view.redact_sensitive_entry(response)
