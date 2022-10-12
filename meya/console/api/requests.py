import logging

from meya.console.api.exceptions import QueryError
from meya.console.api.schema import AccountType
from meya.console.api.schema import AppType
from meya.console.api.schema import Mutation
from meya.console.api.schema import Query
from meya.console.api.schema import UserType
from meya.util.json import to_json
from requests.auth import AuthBase
from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation
from typing import List
from typing import Union
from typing import cast


class TokenAuth(AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, "token", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, request):
        request.headers["Authorization"] = "Token " + self.token
        return request


class CustomRequestsEndpoint(RequestsEndpoint):
    logger = logging.getLogger(__name__)  # Used in base class

    def _log_graphql_error(self, query, data):
        self.logger.debug("GraphQL query: %s", query)
        self.logger.debug("GraphQL data: %s", data)
        raise QueryError(to_json(data, pretty=True))

    def _log_http_error(self, query, req, exc):
        self.logger.debug("GraphQL request: %s", req)
        self.logger.debug("GraphQL query: %s", query)
        raise exc

    def _log_json_error(self, body, exc):
        raise QueryError(body)


class RequestsConsoleApi(CustomRequestsEndpoint):
    logger = logging.getLogger(__name__)  # Used in base class

    def __init__(self, grid_url: str, auth_token: str):
        super().__init__(
            url=f"{grid_url}/console/v2/api/", auth=TokenAuth(auth_token)
        )

    def post(self, op: Operation) -> Union[Query, Mutation]:
        data = self(op)
        return op + data

    def query(self, op: Query) -> Query:
        return self.post(cast(Operation, op))

    def query_user(self, op: Query) -> UserType:
        return self.query(op).user

    def query_accounts(self, op: Query) -> List[AccountType]:
        return self.query_user(op).accounts

    def query_apps(self, op: Query) -> List[AppType]:
        return [
            app for account in self.query_accounts(op) for app in account.apps
        ]

    def mutation(self, op: Mutation) -> Mutation:
        return self.post(cast(Operation, op))
