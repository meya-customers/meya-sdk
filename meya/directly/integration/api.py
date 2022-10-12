import datetime

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from http import HTTPStatus
from meya.directly.payload.payload import DirectlyPayload
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.util.dict import to_dict
from numbers import Real
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Optional
from urllib.parse import quote_plus
from urllib.parse import urlencode


class TokenError(Exception):
    pass


class ApiVersion(Enum):
    V1 = "v1"
    V2 = "v2"


@dataclass
class BearerTokenRequest(DirectlyPayload):
    client_id: str
    client_secret: str
    scope: str
    grant_type: str


@dataclass
class BearerToken(DirectlyPayload):
    access_token: str
    token_type: str
    scope: str
    expires_in: Optional[int] = None
    expiry_date: Optional[datetime.datetime] = None

    def __post_init__(self):
        if not (self.expires_in or self.expiry_date):
            raise TokenError("`expires_in` or `expiry_date` required")
        if not self.expiry_date:
            self.expiry_date = datetime.datetime.utcnow() + datetime.timedelta(
                0, self.expires_in
            )

    @property
    def is_expired(self):
        # leave 60 second buffer
        return (
            self.expiry_date
            < datetime.datetime.utcnow() + datetime.timedelta(0, seconds=60)
        )

    @property
    def as_header(self):
        return f"Bearer {self.access_token}"


@dataclass
class UnderstandNext(DirectlyPayload):
    text: str
    metadata: dict
    language: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self, preserve_nones=False)


@dataclass
class UnderstandPredict(DirectlyPayload):
    text: str


class QuickReply(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Rating(Enum):
    NEGATIVE_5 = "NEGATIVE_5"
    NEUTRAL_NEGATIVE_5 = "NEUTRAL_NEGATIVE_5"
    NEUTRAL_5 = "NEUTRAL_5"
    NEUTRAL_POSITIVE_5 = "NEUTRAL_POSITIVE_5"
    POSITIVE_5 = "POSITIVE_5"


@dataclass
class AutomateMessage(DirectlyPayload):
    text: str


@dataclass
class AutomateFeedback(DirectlyPayload):
    quickReply: QuickReply


@dataclass
class AutomateRate(DirectlyPayload):
    rating: Rating


@dataclass
class ExpertFeedback(DirectlyPayload):
    confirm: bool
    userEmail: str


@dataclass
class ExpertRate(DirectlyPayload):
    rating: Rating
    userEmail: str


class ActorType(Enum):
    EXPERT = "EXPERT"
    POSTER = "POSTER"
    BOT = "BOT"


@dataclass
class Actor(DirectlyPayload):
    type: ActorType
    name: Optional[str] = field(default=None)
    handle: Optional[str] = field(default=None)
    avatarUrl: Optional[str] = field(default=None)
    refId: Optional[str] = field(default=None)


@dataclass
class ConversationMessage(DirectlyPayload):
    text: str
    actor: Actor
    metadata: Optional[dict] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self, preserve_nones=False)


@dataclass
class ConversationRate(DirectlyPayload):
    rating: Rating
    userRefId: str


@dataclass
class ConversationResolve(DirectlyPayload):
    confirm: bool
    userRefId: str


@dataclass
class DirectlyApi(Api):
    domain: str
    client_id: str
    client_secret: str
    version: ApiVersion = ApiVersion.V2
    timeout: Real = 6

    # token singletons
    _bearer_tokens: ClassVar[dict] = {}

    async def new_token(self) -> BearerToken:
        res = await self.http.post(
            url=f"{self.api_root}/oauth/token",
            timeout=self.timeout,
            data=BearerTokenRequest(
                client_id=self.client_id,
                client_secret=self.client_secret,
                scope="read write",
                grant_type="client_credentials",
            ).to_dict(),
        )
        if res.status in (HTTPStatus.OK, HTTPStatus.CREATED):
            try:
                return BearerToken(**res.data)
            except TypeError:
                raise TokenError("Unexpected response JSON.")
        else:
            raise TokenError(f"Token refresh error. {res.status} {res.data}")

    # v2 engage interfaces
    async def new_conversation(
        self,
        text: str,
        user_name: Optional[str] = None,
        user_ref_id: Optional[str] = None,
    ) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/engage/conversation/message",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=ConversationMessage(
                actor=Actor(
                    type=ActorType.POSTER, name=user_name, refId=user_ref_id
                ),
                text=text,
                metadata={"internal": {"useAirResponse": False}},
            ).to_dict(),
        )

    async def conversation_message(
        self, text: str, conversation_id: str, user_ref_id: str
    ) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/engage/conversation/{conversation_id}/message",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=ConversationMessage(
                actor=Actor(type=ActorType.POSTER, refId=user_ref_id),
                text=text,
            ).to_dict(),
        )

    async def conversation_resolve(
        self, message_id: str, confirm: bool, user_ref_id: str
    ) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/engage/conversation/message/{message_id}/resolve",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=ConversationResolve(
                confirm=confirm, userRefId=user_ref_id
            ).to_dict(),
        )

    async def conversation_rate(
        self, conversation_id: str, rating: Rating, user_ref_id: str
    ) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/engage/conversation/{conversation_id}/rate",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=ConversationRate(
                rating=rating, userRefId=user_ref_id
            ).to_dict(),
        )

    async def understand_next(
        self, text: str, language: Optional[str] = None
    ) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/understand/next",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=UnderstandNext(
                text=text,
                metadata={"private": {"meya": True}},
                language=language,
            ).to_dict(),
        )

    async def understand_predict(self, text: str) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/understand/predict",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=UnderstandPredict(text=text).to_dict(),
        )

    async def automate_post_message(self, text: str) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/automate/conversation/message",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=AutomateMessage(text=text).to_dict(),
        )

    async def automate_feedback(
        self, answer_uuid: str, quick_reply: QuickReply
    ) -> HttpResponseEntry:
        return await self.http.post(
            url=f"{self.api_root_with_version}/automate/conversation/message/{answer_uuid}/feedback",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=AutomateFeedback(quickReply=quick_reply).to_dict(),
        )

    async def automate_rate(
        self, answer_uuid: str, rating: Rating
    ) -> HttpResponseEntry:
        # TODO: validate once this API live (currently untested)
        return await self.http.post(
            url=f"{self.api_root_with_version}/automate/conversation/{answer_uuid}/rate",
            headers=await self._get_headers(),
            timeout=self.timeout,
            json=AutomateRate(rating=rating).to_dict(),
        )

    @property
    def api_root(self) -> str:
        return f"https://{self.domain}"

    @property
    def api_root_with_version(self) -> str:
        return f"{self.api_root}/{self.version.value}"

    async def _get_headers(self) -> dict:
        token = await self._get_bearer_token()
        return {
            "Content-Type": "application/json",
            "Authorization": token.as_header,
        }

    async def _get_bearer_token(self) -> BearerToken:
        bearer_token = self._bearer_tokens.get(self.client_id)
        if bearer_token and not bearer_token.is_expired:
            return bearer_token
        bearer_token = await self.new_token()
        self._bearer_tokens[self.client_id] = bearer_token
        return bearer_token

    @staticmethod
    def urlencode(data: dict) -> str:
        return urlencode(data, quote_via=quote_plus)
