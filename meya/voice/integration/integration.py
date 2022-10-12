import re

from dataclasses import dataclass
from meya.bot.entry import BotEntry
from meya.button.event.click import ButtonClickEvent
from meya.db.view.thread import ThreadView
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.entry import Entry
from meya.event.entry import Event
from meya.flow.entry.end import FlowEndEntry
from meya.form.event.ask import FormAskEvent
from meya.form.event.error import FormErrorEvent
from meya.form.event.submit import FormSubmitEvent
from meya.http.entry.request import HttpRequestEntry
from meya.integration.element.interactive import InteractiveIntegration
from meya.orb.event.hero import HeroEvent
from meya.text.event import TextEvent
from meya.text.event.say import SayEvent
from meya.trigger.entry.activate import TriggerActivateEntry
from typing import List
from typing import Optional
from typing import Union


@dataclass
class VoiceIntegration(InteractiveIntegration):
    is_abstract: bool = meta_field(value=True)

    entry: Union[
        HttpRequestEntry, FlowEndEntry, TriggerActivateEntry
    ] = process_field()

    async def process(self) -> List[Entry]:
        with self.current.set(self):
            if self.request:
                # TODO: block requests that have the wrong method
                return await self.rx()
            elif (
                isinstance(self.entry, FlowEndEntry)
                and len(self.entry.stack) == 0
            ):
                return await self.tx()
            elif isinstance(self.entry, TriggerActivateEntry):
                return await self.tx()
            else:
                return []

    async def get_thread_events(
        self, session: ThreadView, entry: BotEntry
    ) -> List[Event]:
        voice_next_tx_event_id = session.voice_next_tx_event_id or "-"
        events = await self.history.get_thread_events(
            entry.thread_id, start=voice_next_tx_event_id, count=256
        )
        prev_event = next(iter(events), None)
        if prev_event:
            session.voice_next_tx_event_id = prev_event.incremented_entry_id
        return list(
            reversed(
                [event for event in events if event.integration_id != self.id]
            )
        )

    def get_text_from_events(self, events: List[Event]) -> str:
        return " ".join([self.get_text_from_event(event) for event in events])

    def get_text_from_event(self, event: Event) -> str:
        if isinstance(event, TextEvent):
            return event.text
        elif isinstance(event, HeroEvent):
            return f"{event.title}. {event.description}"
        elif isinstance(event, FormAskEvent):
            labels = " ".join([field.label for field in event.fields])
            return f"{event.text} {labels}"
        elif isinstance(event, FormErrorEvent):
            return " ".join([text for text in event.fields.values()])
        else:
            return ""

    def get_forms(self, events: List[Entry]) -> Optional[List[dict]]:
        if any(True for event in events if isinstance(event, FormErrorEvent)):
            # Do not reset the forms if there was a form error
            return None

        return [
            self.get_form_from_event(event)
            for event in events
            if isinstance(event, FormAskEvent)
        ]

    def get_form_from_event(self, event: FormAskEvent) -> dict:
        return dict(
            form_id=event.form_id,
            fields=[field.name for field in event.fields],
        )

    def is_ssml(self, text: str) -> bool:
        if re.search("</|/>", text):
            return True
        else:
            return False

    def get_event_from_text(
        self, forms: List[dict], quick_replies: List[dict], text: str
    ) -> Union[FormSubmitEvent, ButtonClickEvent, SayEvent]:
        form_submit = self.get_form_submit_event(forms=forms, text=text)
        if form_submit:
            return form_submit

        button_click_event = self.get_button_click_event(
            quick_replies=quick_replies, text=text
        )
        if button_click_event:
            return button_click_event

        return SayEvent(text=text)

    def get_form_submit_event(
        self, forms: List[dict], text: str
    ) -> Optional[FormSubmitEvent]:
        for form in forms:
            form_id = form.get("form_id")
            fields = form.get("fields")
            if form_id is None or fields is None:
                continue
            return FormSubmitEvent(
                form_id=form_id, fields={field: text for field in fields}
            )

    def get_button_click_event(
        self, quick_replies: List[dict], text: str
    ) -> Optional[ButtonClickEvent]:
        for quick_reply in quick_replies:
            button_text = quick_reply.get("text", "")
            button_id = quick_reply.get("button_id")
            if text.lower() == button_text.lower() and button_id:
                return ButtonClickEvent(button_id=button_id, text=None)
