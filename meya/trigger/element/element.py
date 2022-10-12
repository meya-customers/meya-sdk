from dataclasses import MISSING
from dataclasses import dataclass
from meya.bot.element import Bot
from meya.bot.element import BotRef
from meya.component.entry.start import ComponentStartEntry
from meya.component.spec import ActionComponentSpec
from meya.component.spec import ComponentSpec
from meya.core.abstract_type_registry import AbstractTypeRegistry
from meya.core.meta_level import MetaLevel
from meya.db.view.thread import ThreadMode
from meya.db.view.user import UserType
from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event.entry import Event
from meya.icon.spec import IconElementSpecUnion
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.trigger.entry.match import TriggerMatchEntry
from meya.util.dict import MISSING_FACTORY
from meya.util.dict import to_dict
from numbers import Real
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class TriggerResponse:
    result: Any = response_field(sensitive=True)


@dataclass
class TriggerActionEntry:
    entry: Dict[str, Any]


@dataclass
class TriggerMatchResult:
    pass


@dataclass
class TriggerMatchSuccessResult(TriggerMatchResult):
    confidence: Real
    data: Any


@dataclass
class TriggerMatchFailureResult(TriggerMatchResult):
    pass


@dataclass
class Trigger(Element):
    MAX_CONFIDENCE = 1.0
    MIN_CONFIDENCE = 0.001
    NO_CONFIDENCE = 0.0
    # TODO: convert this to a config property
    EVENT_KEY = "event"
    RESULT_KEY = "result"
    CONFIDENCE_KEY = "confidence"
    ORIGINAL_CONFIDENCE_KEY = "original_confidence"

    is_abstract: bool = meta_field(value=True)
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/49-move/cursor-move-right.svg"
    )

    bot: Optional[BotRef] = element_field(
        default=None,
        help="Bot used to evaluate this trigger",
        level=MetaLevel.ADVANCED,
    )
    action: Union[TriggerActionEntry, ActionComponentSpec] = element_field(
        help="Action executed if this trigger matches",
        level=MetaLevel.VERY_BASIC,
    )
    when: Any = element_field(
        default_factory=MISSING_FACTORY,
        help="Custom condition for when to evaluate this trigger",
        level=MetaLevel.INTERMEDIATE,
    )
    confidence: Optional[Real] = element_field(
        default=None,
        help="Custom confidence override value for trigger matches",
        level=MetaLevel.ADVANCED,
    )
    entry: Event = process_field()
    encrypted_entry: Event = process_field()

    async def accept(self) -> bool:
        if not await super().accept():
            return False
        bot = Bot.current.get()
        if not self.bot and not bot.default:
            return False
        if self.bot and self.bot.ref != bot.id:
            return False
        if self.when is not MISSING:
            return bool(self.when)
        if self.spec and self.spec.trigger_when is not MISSING:
            return bool(self.spec.trigger_when)
        return await self.default_when()

    async def accept_sensitive(self) -> bool:
        return await self.accept()

    async def default_when(self) -> bool:
        if self.entry.sensitive:
            return False
        if self.event_user.type != UserType.USER:
            return False
        if self.thread.mode == ThreadMode.BOT:
            return True
        else:
            return False

    async def process(self) -> List[Entry]:
        result = await self.match()
        if isinstance(result, TriggerMatchSuccessResult):
            entry = await self._succeed(result.confidence, result.data)
        else:
            entry = self._fail()
        return [entry]

    async def match(self) -> TriggerMatchResult:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    def succeed(
        self, *, confidence: Real = MAX_CONFIDENCE, data: Any = None
    ) -> TriggerMatchSuccessResult:
        return TriggerMatchSuccessResult(confidence=confidence, data=data)

    async def _succeed(self, confidence: Real, data: Any) -> TriggerMatchEntry:
        if self.entry.sensitive and self.db.config.event_ledger.sensitive_ttl:
            data = await self.db.encrypt_sensitive_fields(
                data, preserve_nones=True
            )
        result_data = {
            self.CONFIDENCE_KEY: confidence,
            self.EVENT_KEY: self.encrypted_entry.to_typed_dict(),
        }
        if self.confidence is not None:
            # TODO: Change QuickType to allow any float-convertible for
            #       "number" properties or just use Real like here
            result_data.update(
                {
                    self.CONFIDENCE_KEY: self.confidence,
                    self.ORIGINAL_CONFIDENCE_KEY: confidence,
                }
            )
            confidence = self.confidence
        if data is None:
            data = result_data
        else:
            data = {**result_data, **to_dict(data, preserve_nones=True)}
        if isinstance(self.action, ComponentSpec):
            action_entry = ComponentStartEntry(
                data=data,
                flow=None,
                index=None,
                spec=to_dict(self.action),
                stack=None,
            ).to_typed_dict()
        else:
            action_entry = {
                **self.action.entry,
                "data": {
                    **self.action.entry["data"],
                    "data": {**self.action.entry["data"]["data"], **data},
                },
            }
        return TriggerMatchEntry(
            confidence=confidence, action_entry=action_entry
        )

    def fail(self) -> TriggerMatchFailureResult:
        return TriggerMatchFailureResult()

    def _fail(self) -> TriggerMatchEntry:
        return TriggerMatchEntry(
            confidence=self.NO_CONFIDENCE, action_entry=None
        )

    def activate(
        self, type_registry: Optional[AbstractTypeRegistry] = None
    ) -> TriggerActivateEntry:
        return TriggerActivateEntry(
            spec=to_dict(TriggerSpec.from_element(self, type_registry))
        )


@dataclass
class TriggerSpec(Spec):
    element_type: ClassVar[Type[Element]] = Trigger

    snippet_default: str = meta_field(value="catchall")


class TriggerRef(Ref):
    element_type: ClassVar[Type[Element]] = Trigger


@dataclass
class FlowTriggerSpec(TriggerSpec):
    meta_name: str = meta_field(value="Trigger")
    snippet_default: str = meta_field(value="catchall")


@dataclass
class ComponentTriggerSpec(TriggerSpec):
    meta_name: str = meta_field(value="Trigger")
    snippet_default: str = meta_field(value="catchall")
