import aiohttp
import json
import logging

from aiohttp import ClientResponseError
from dataclasses import dataclass
from meya.console.api.exceptions import QueryError
from meya.console.api.schema import AccountType
from meya.console.api.schema import AppType
from meya.console.api.schema import Mutation
from meya.console.api.schema import Query
from meya.console.api.schema import UserType
from meya.db.view.http import AuthBase
from meya.db.view.http import TokenAuth
from meya.util.json import to_json
from sgqlc.endpoint.base import BaseEndpoint
from sgqlc.operation import Operation
from typing import List
from typing import Union
from typing import cast


@dataclass
class AiohttpEndpoint(BaseEndpoint):
    logger = logging.getLogger(__name__)  # Used in base class

    session: aiohttp.ClientSession
    timeout: int

    @property
    def url(self) -> str:
        raise NotImplementedError()

    @property
    def auth(self) -> AuthBase:
        raise NotImplementedError()

    async def __call__(
        self,
        query,
        variables=None,
        operation_name=None,
        extra_headers=None,
        timeout=None,
    ):
        if isinstance(query, bytes):
            query = query.decode("utf-8")
        elif not isinstance(query, str):
            # allows sgqlc.operation.Operation to be passed
            # and generate compact representation of the queries
            query = bytes(query).decode("utf-8")

        headers = (extra_headers or {}).copy()
        if "Accept" not in headers:
            headers["Accept"] = "application/json; charset=utf-8"
        headers.update({"Content-Type": "application/json; charset=utf-8"})
        headers = self.auth(headers or {})

        request_data = {
            "query": query,
            "variables": variables,
            "operationName": operation_name,
        }

        self.logger.debug("Query:\n%s", query)

        try:
            response = await self.session.post(
                self.url,
                json=request_data,
                headers=headers,
                timeout=timeout or self.timeout,
                allow_redirects=False,
            )
            if response.status >= 400:
                raise ClientResponseError(
                    response.request_info,
                    response.history,
                    status=response.status,
                    message=await response.text() or response.reason,
                    headers=response.headers,
                )
            try:
                data = await response.json()
                if data and data.get("errors"):
                    return self._log_graphql_error(query, data)
                return data
            except json.JSONDecodeError as exc:
                return self._log_json_error(await response.text(), exc)
        except aiohttp.ClientResponseError as exc:
            return self._log_http_error(
                query, exc.request_info, exc.history, exc
            )

    def _log_graphql_error(self, query, data):
        self.logger.debug("GraphQL query: %s", query)
        self.logger.debug("GraphQL data: %s", data)
        raise QueryError(to_json(data, pretty=True))

    def _log_http_error(self, query, req, history, exc):
        self.logger.debug("GraphQL request: %s", req)
        self.logger.debug("GraphQL history: %s", history)
        self.logger.debug("GraphQL query: %s", query)
        raise exc

    def _log_json_error(self, body, exc):
        raise QueryError(body)


@dataclass
class AiohttpAppApi(AiohttpEndpoint):
    pod_ip: str
    auth_token: str

    @property
    def url(self) -> str:
        return f"http://{self.pod_ip}:7070/graphql"

    @property
    def auth(self) -> AuthBase:
        return TokenAuth(self.auth_token)


@dataclass
class AiohttpConsoleApi(AiohttpEndpoint):
    grid_url: str
    auth_token: str

    @property
    def url(self) -> str:
        return f"{self.grid_url}/console/v2/api/"

    @property
    def auth(self) -> AuthBase:
        return TokenAuth(self.auth_token)

    async def post(self, op: Operation) -> Union[Query, Mutation]:
        data = await self(op)
        return op + data

    async def query(self, op: Query) -> Query:
        return await self.post(cast(Operation, op))

    async def query_user(self, op: Query) -> UserType:
        return (await self.query(op)).user

    async def query_accounts(self, op: Query) -> List[AccountType]:
        return (await self.query_user(op)).accounts

    async def query_apps(self, op: Query) -> List[AppType]:
        return [
            app
            for account in await self.query_accounts(op)
            for app in account.apps
        ]

    async def mutation(self, op: Mutation) -> Mutation:
        return await self.post(cast(Operation, op))
