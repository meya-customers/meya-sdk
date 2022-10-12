import meya.util.uuid

from dataclasses import dataclass
from dataclasses import field
from meya.button.event.click import ButtonClickEvent
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonEventSpec
from meya.button.spec import ButtonType
from meya.calendly.event.invitee.created import CalendlyInviteeCreatedEvent
from meya.calendly.integration import CalendlyIntegration
from meya.calendly.integration import CalendlyIntegrationRef
from meya.calendly.payload.payload import CalendlyEventType
from meya.calendly.payload.payload import CalendlyEventV2
from meya.calendly.payload.payload import CalendlyWebhook
from meya.calendly.trigger import CalendlyTrigger
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.text.event.say import SayEvent
from meya.tile.event.ask import TileAskEvent
from meya.tile.spec import TileButtonStyle
from meya.tile.spec import TileCell
from meya.tile.spec import TileEventSpec
from meya.tile.spec import TileImage
from meya.trigger.element import Trigger
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import to_dict
from meya.util.enum import SimpleEnum
from meya.util.generate_id import generate_button_id
from meya.util.json import to_json
from typing import List
from typing import Optional
from typing import Union


class CalendlyState(SimpleEnum):
    INITIAL = "initial"
    CLOSED = "closed"
    PENDING = "pending"
    BOOKED = "booked"


@dataclass
class CalendlyComponentResponse:
    result: Optional[
        Union[CalendlyWebhook, CalendlyEventV2]
    ] = response_field()


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class CalendlyComponent(InteractiveComponent):
    BOOKING_ID_KEY = "calendly_component_booking_id"
    POPUP_CLOSED_BUTTON_ID_KEY = "calendly_component_popup_closed_button_id"
    EVENT_SCHEDULED_BUTTON_ID_KEY = (
        "calendly_component_event_scheduled_button_id"
    )
    STATE_KEY = "calendly_component_state"

    # calendly fields. example: "erik-meya/meya-demo"
    calendly: str = element_field(signature=True)
    integration: Optional[CalendlyIntegrationRef] = element_field(
        default=None,
        help="The Calendly integration to use for booking confirmation",
    )

    # text copy
    button_text: str = element_field(default="Book a meeting")
    closed_text: str = element_field(
        default="No longer interested in booking a meeting?"
    )
    pending_text: str = element_field(default="Completing the booking...")
    try_again_text: str = element_field(default="I'm still interested")
    cancel_text: str = element_field(default="Not interested")

    prefill: Optional[dict] = element_field(default=None)
    utm_source: str = element_field(default="meya")
    utm_campaign: Optional[str] = element_field(default=None)
    utm_medium: Optional[str] = element_field(default=None)
    utm_term: Optional[str] = element_field(default=None)

    ask: Optional[str] = element_field(default=None)

    # tile spec fields
    title: Optional[str] = element_field(default=None)
    description: Optional[str] = element_field(default=None)
    image: Optional[TileImage] = element_field(default=None)
    rows: List[List[TileCell]] = element_field(default_factory=list)
    button_style: Optional[TileButtonStyle] = element_field(default=None)

    # common fields
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )

    # component state variables. set on init(). cleared on reset()
    state: CalendlyState = process_field(default=None)
    booking_id: str = process_field(default=None)
    popup_closed_button_id: str = process_field(default=None)
    event_scheduled_button_id: str = process_field(default=None)

    async def start(self) -> List[Entry]:
        self.reset()
        return await self.start_or_next()

    async def next(self) -> List[Entry]:
        return await self.start_or_next()

    async def start_or_next(self) -> List[Entry]:
        self.init()

        cancel_button = ButtonElementSpec(
            type=ButtonType.FLOW_NEXT,
            text=self.cancel_text,
            data=to_dict(
                CalendlyComponentResponse(result=None), preserve_nones=True
            ),
        )
        try_again_button = ButtonElementSpec(
            type=ButtonType.COMPONENT_NEXT,
            text=self.try_again_text,
            data=self._state_data(CalendlyState.INITIAL),
        )
        _, [popup_closed_trigger] = ButtonEventSpec.from_element_spec_union(
            ButtonElementSpec(
                type=ButtonType.COMPONENT_NEXT,
                # text is unused
                text="calendly.popup_closed",
                button_id=self.popup_closed_button_id,
                data=self._state_data(CalendlyState.CLOSED),
            )
        )
        _, [event_scheduled_trigger] = ButtonEventSpec.from_element_spec_union(
            ButtonElementSpec(
                type=ButtonType.COMPONENT_NEXT,
                # text is unused
                text="calendly.event_scheduled",
                button_id=self.event_scheduled_button_id,
                data=self._state_data(
                    CalendlyState.BOOKED
                    if self.integration
                    else CalendlyState.PENDING
                ),
            )
        )
        if self.state == CalendlyState.INITIAL:
            calendly_button = ButtonElementSpec(
                type=ButtonType.STATIC,
                text=self.button_text,
                javascript=self._javascript(),
            )
            buttons, triggers = ButtonEventSpec.from_element_spec_union_list(
                [calendly_button, cancel_button]
            )
            calendar_tile = TileEventSpec(
                buttons=buttons,
                description=self.description,
                image=self.image,
                rows=self.rows,
                title=self.title,
            )

            ask_tiles_event = TileAskEvent(
                button_style=self.button_style,
                layout=None,
                text=self.ask,
                tiles=[calendar_tile],
            )
            return self.respond(
                ask_tiles_event,
                *triggers,
                self._calendly_trigger(),
                popup_closed_trigger,
                event_scheduled_trigger,
            )

        elif self.state == CalendlyState.CLOSED:
            (
                quick_replies,
                quick_reply_triggers,
            ) = ButtonEventSpec.from_element_spec_union_list(
                [try_again_button, cancel_button]
            )
            say_event = SayEvent(
                text=self.closed_text, quick_replies=quick_replies
            )
            return self.respond(
                say_event, *quick_reply_triggers, self._calendly_trigger()
            )

        elif self.state == CalendlyState.PENDING:
            say_event = SayEvent(text=self.pending_text)
            return self.respond(say_event, self._calendly_trigger())

        elif self.state == CalendlyState.BOOKED:
            # success!
            self.reset()
            try:
                event = Entry.from_typed_dict(
                    self.entry.data.pop(Trigger.EVENT_KEY, None)
                )
                if self.integration:
                    assert isinstance(event, ButtonClickEvent)
                    calendly_event_id = event.context["calendly_event_id"]
                    integration: CalendlyIntegration = await self.resolve(
                        self.integration
                    )
                    result = await integration.api.get_event(calendly_event_id)
                else:
                    assert isinstance(event, CalendlyInviteeCreatedEvent)
                    result = CalendlyWebhook.from_dict(event.data)
            except:
                self.log.exception()
                result = None
            return self.respond(data=CalendlyComponentResponse(result=result))

        else:
            raise NotImplementedError

    def init(self):
        # booking_id
        new_booking_id = self.generate_booking_id()
        self.booking_id = (
            self.entry.data.get(self.BOOKING_ID_KEY) or new_booking_id
        )
        # popup_closed_button_id
        new_popup_closed_button_id = generate_button_id()
        self.popup_closed_button_id = (
            self.entry.data.get(self.POPUP_CLOSED_BUTTON_ID_KEY)
            or new_popup_closed_button_id
        )
        # event_scheduled_button_id
        new_event_scheduled_button_id = generate_button_id()
        self.event_scheduled_button_id = (
            self.entry.data.get(self.EVENT_SCHEDULED_BUTTON_ID_KEY)
            or new_event_scheduled_button_id
        )
        # state
        self.state = CalendlyState(
            self.entry.data.get(self.STATE_KEY) or CalendlyState.INITIAL
        )

    def reset(self):
        self.entry.data.pop(self.BOOKING_ID_KEY, None)
        self.entry.data.pop(self.POPUP_CLOSED_BUTTON_ID_KEY, None)
        self.entry.data.pop(self.EVENT_SCHEDULED_BUTTON_ID_KEY, None)
        self.entry.data.pop(self.STATE_KEY, None)

    def _javascript(self) -> str:
        lifecycle_buttons = {
            "popupClosed": self.popup_closed_button_id,
            "eventScheduled": self.event_scheduled_button_id,
        }

        popup_options = dict(
            url=f"https://calendly.com/{self.calendly}",
            utm=self._utm_parameters(),
        )
        if self.prefill:
            popup_options["prefill"] = self.prefill

        lifecycle_javascript = self.generate_lifecycle_javascript()
        return (
            f"var lifecycleButtons = {to_json(lifecycle_buttons)};"
            f"var popupOptions = {to_json(popup_options)};"
            f"{lifecycle_javascript}"
        )

    def _utm_parameters(self) -> dict:
        """
        utm_source: required default: "meya" can be overridden
        utm_content: required can't be overridden. Set to thread.id
        utm_campaign: optional, str
        utm_medium: optional, str
        utm_term: optional, str
        """
        return dict(
            utmCampaign=self.utm_campaign,
            utmSource=self.utm_source,
            utmMedium=self.utm_medium,
            utmContent=CalendlyWebhook.encode_utm_content(
                self.thread.id, self.user.id, booking_id=self.booking_id
            ),
            utmTerm=self.utm_term,
        )

    def _calendly_trigger(self) -> TriggerActivateEntry:
        return CalendlyTrigger(
            calendly_event=CalendlyEventType.INVITEE_CREATED.value,
            booking_id=self.booking_id,
            action=self.get_next_action(
                data=self._state_data(CalendlyState.BOOKED)
            ),
        ).activate()

    def _state_data(self, state: CalendlyState) -> dict:
        return {
            self.BOOKING_ID_KEY: self.booking_id,
            self.POPUP_CLOSED_BUTTON_ID_KEY: self.popup_closed_button_id,
            self.EVENT_SCHEDULED_BUTTON_ID_KEY: self.event_scheduled_button_id,
            self.STATE_KEY: state,
        }

    @staticmethod
    def generate_booking_id() -> str:
        return f"bk-{meya.util.uuid.uuid4_hex()}"

    @staticmethod
    def generate_lifecycle_javascript() -> str:
        """
        https://help.calendly.com/hc/en-us/articles/360020052833-Advanced-embed-options
        lifecycle events example: orb.click(':button_id', ':text')
        """
        return """
            var overlayElement;
            var mutationObserver;
            
            function onMutation() {
                if (!overlayElement.parentElement) {
                    orb.click(
                        lifecycleButtons.popupClosed,
                        "calendly.popup_closed"
                    );
                    window.removeEventListener('message', onWindowMessage);
                    mutationObserver.disconnect();
                }
            }
            
            function onWindowMessage(e) {
                if (e.data.event === 'calendly.event_scheduled') {
                    orb.click(
                        lifecycleButtons.eventScheduled,
                        "calendly.event_scheduled",
                        { calendly_event_id: e.data.payload.event.uri.replace(/^.*\//, '')}
                    );
                    Calendly.closePopupWidget();
                    window.removeEventListener('message', onWindowMessage);
                    if (mutationObserver) {
                        mutationObserver.disconnect();
                    }
                }
            }
            
            Calendly.initPopupWidget(popupOptions);

            try {
                window.addEventListener('message', onWindowMessage);
                overlayElement = document.querySelector('.calendly-overlay');
                mutationObserver = new MutationObserver(onMutation);
                mutationObserver.observe(
                    overlayElement.parentElement,
                    { childList: true }
                );
            } catch (err) {
                console.error(err);
            }
            """
