from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.front.payload.teammate import FrontTeammateGet
from meya.http.payload.field import payload_field


"""
https://dev.frontapp.com/reference/comments
"""


@dataclass
class FrontCommentGet(FrontPayload):
    author: FrontTeammateGet = payload_field()
    body: str = payload_field()
