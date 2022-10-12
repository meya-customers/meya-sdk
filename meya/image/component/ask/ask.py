from dataclasses import dataclass
from dataclasses import field
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.image.trigger import ImageTrigger
from meya.text.event.ask import AskEvent
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.IMAGE)
    visibility: Optional[ComposerVisibility] = field(
        default=ComposerVisibility.SHOW
    )


class Expect(SimpleEnum):
    IMAGE = "image"


@dataclass
class ImageAskComponent(InteractiveComponent):
    ask: Optional[str] = element_field(signature=True)
    expect: Optional[Expect] = element_field(signature=True, default=None)
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )

    async def start(self) -> List[Entry]:
        ask_event = AskEvent(text=self.ask)

        return self.respond(
            ask_event, ImageTrigger(action=self.get_next_action()).activate()
        )
