import datetime

from dataclasses import dataclass
from http import HTTPStatus
from meya.db.view.http import HttpError
from meya.entry import Entry
from meya.event.entry import Event
from meya.http.entry import HttpEntry
from meya.text.event.say import SayEvent
from meya.voice.integration.integration import VoiceIntegration
from typing import ClassVar
from typing import List


@dataclass
class StatusIntegration(VoiceIntegration):
    NAME: ClassVar[str] = "status"

    async def rx(self) -> List[Entry]:
        integration_user_id = self.request.params.get("user_id")
        text = self.request.params.get("text")

        if not integration_user_id or not text:
            return self.respond(
                data=dict(ok=False, error="`user_id` and `text` required."),
                status=HTTPStatus.BAD_REQUEST,
            )

        await self.event_user.identify(integration_user_id)
        await self.thread.identify(
            integration_user_id,
            default_data=dict(primary_user_id=self.event_user.id),
            data=dict(voice=True),
        )

        return [SayEvent(text=text)]

    async def tx(self) -> List[Entry]:
        integration_user_id = await self.thread.try_reverse_lookup()
        if not integration_user_id:
            return []

        events = await self._get_status_event_history()
        text = self.get_text_from_events(
            [event for event in events if event.integration_id != self.id]
        )
        request_id = await self._get_request_id(events)

        return [
            self.create_response(
                request_id=request_id,
                status=HTTPStatus.OK,
                data=dict(
                    ok=True, text=text, time=str(datetime.datetime.utcnow())
                ),
                url=self.gateway_webhook_url,
            )
        ]

    async def _get_status_event_history(self) -> List[Event]:
        # TODO: switch to trace id traversal
        events = await self.history.get_thread_events(
            self.entry.thread_id, end="+", count=32
        )
        return list(
            reversed(
                [
                    event
                    for event in events
                    if event.trace_id == self.entry.trace_id
                ]
            )
        )

    async def _get_request_id(self, events: List[Event]) -> str:
        """Iterate back through events and find the first event
        whose parent is an http ledger entry with a request_id
        This represents the "causal" event that contains the reference
        to the http request and it's request_id. Limit the search
        to events with the same trace_id

        This can be deprecated once there is an api to traverse the
        entire ledger tree for a given trace_id
        """
        for event in events:
            if (
                event.parent_entry_ref.ledger == HttpEntry.get_entry_ledger()
                and event.trace_id == self.entry.trace_id
            ):
                request_id = event.parent_entry_ref.data.get("request_id")
                if request_id:
                    return request_id
        raise HttpError("No event with request_id found")
