import asyncio

from contextlib import AbstractContextManager
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict


@dataclass
class AsyncRequestCollection:
    timeout: int = field(default=0)
    active_requests: Dict[str, asyncio.Future] = field(
        init=False, default_factory=dict
    )

    @contextmanager
    def begin_request(self, request: Any) -> AbstractContextManager:
        request_id = request.request_id
        future = self.active_requests.get(request_id)
        if not future:
            future = asyncio.get_running_loop().create_future()
            self.active_requests[request_id] = future

        async def response_future(custom_timeout: int = 0):
            return await asyncio.wait_for(
                future, custom_timeout or self.timeout
            )

        try:
            yield response_future
        finally:
            self.active_requests.pop(request_id, None)

    def complete_request(self, response: Any) -> None:
        request_id = response.request_id
        future = self.active_requests.get(request_id)
        if future and not future.done():
            future.set_result(response)
