from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from meya.zendesk.support.payload import ZendeskSupportPayload
from typing import Optional


class ZendeskTargetMethod(SimpleEnum):
    GET = "get"
    PATCH = "patch"
    PUT = "put"
    POST = "post"
    DELETE = "delete"


class ZendeskTargetTypes(SimpleEnum):
    URL_TARGET_V2 = "url_target_v2"
    HTTP_TARGET = "http_target"
    # TODO: implement other types


@dataclass
class ZendeskSupportTargetBase(ZendeskSupportPayload):
    """
    https://developer.zendesk.com/rest_api/docs/support/targets#json-format
    """

    type: Optional[str] = payload_field(default=None)
    title: Optional[str] = payload_field(default=None)
    active: Optional[bool] = payload_field(default=None)
    email: Optional[str] = payload_field(default=None)
    subject: Optional[str] = payload_field(default=None)
    created_at: Optional[str] = payload_field(default=None)

    # TODO: implement other types

    # http_target
    target_url: Optional[str] = payload_field(default=None)
    method: Optional[ZendeskTargetMethod] = payload_field(default=None)
    username: Optional[str] = payload_field(default=None)
    password: Optional[str] = payload_field(default=None)
    content_type: Optional[str] = payload_field(default=None)

    @property
    def is_valid_meya_target(self) -> bool:
        return (
            self.type == ZendeskTargetTypes.URL_TARGET_V2.value
            and self.method == ZendeskTargetMethod.POST
            and self.username == "meya"
            and self.content_type == "application/json"
        )


@dataclass
class ZendeskSupportTargetGet(ZendeskSupportTargetBase):
    id: int = payload_field()


@dataclass
class ZendeskSupportTargetUpdate(ZendeskSupportTargetBase):
    pass
