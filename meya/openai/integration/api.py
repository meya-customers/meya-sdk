from dataclasses import dataclass
from http import HTTPStatus
from meya.db.view.http import BearerAuth
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.openai.integration.payload import OpenaiChatCompletionRequest
from meya.openai.integration.payload import OpenaiChatCompletionResponse
from meya.openai.integration.payload import OpenaiCompletionRequest
from meya.openai.integration.payload import OpenaiCompletionResponse
from meya.openai.integration.payload import OpenaiEmbeddingRequest
from meya.openai.integration.payload import OpenaiEmbeddingResponse
from typing import Optional
from typing import Tuple

API_ROOT = "https://api.openai.com/v1"


@dataclass
class OpenaiApi(Api):
    api_key: str
    api_root: str = API_ROOT

    @property
    def auth(self) -> BearerAuth:
        return BearerAuth(self.api_key)

    async def create_completion(
        self,
        completion_request: OpenaiCompletionRequest,
        **kwargs,
    ) -> OpenaiCompletionResponse:
        response = await self.post(
            url=f"{self.api_root}/completions",
            auth=self.auth,
            json=completion_request.to_dict(),
            timeout=20.0,
            **kwargs,
        )
        return OpenaiCompletionResponse.from_dict(response.data)

    async def create_chat_completion(
        self,
        chat_completion_request: OpenaiChatCompletionRequest,
        **kwargs,
    ) -> OpenaiChatCompletionResponse:
        response = await self.post(
            url=f"{self.api_root}/chat/completions",
            auth=self.auth,
            json=chat_completion_request.to_dict(),
            timeout=20.0,
            **kwargs,
        )
        return OpenaiChatCompletionResponse.from_dict(response.data)

    async def create_embedding(
        self,
        embedding_request: OpenaiEmbeddingRequest,
        **kwargs,
    ) -> OpenaiEmbeddingResponse:
        response = await self.post(
            url=f"{self.api_root}/embeddings",
            auth=self.auth,
            json=embedding_request.to_dict(),
            timeout=10.0,
            **kwargs,
        )
        return OpenaiEmbeddingResponse.from_dict(response.data)

    async def post(
        self,
        *args,
        expected: Tuple[int] = (
            HTTPStatus.OK,
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.NOT_FOUND,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.FORBIDDEN,
        ),
        **kwargs,
    ) -> HttpResponseEntry:
        return await self.request("POST", *args, expected=expected, **kwargs)

    async def request(
        self,
        *args,
        expected: Optional[Tuple[int]] = None,
        **kwargs,
    ) -> HttpResponseEntry:
        response = await self.http.send(
            self.http.make_request_entry(*args, **kwargs)
        )
        if expected is not None:
            response.check_status(*expected)
        return response
