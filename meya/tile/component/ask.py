from dataclasses import dataclass
from dataclasses import field
from meya.bot.meta_tag import BotOutputTag
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.tile.event.ask import TileAskEvent
from meya.tile.spec import TileButtonStyle
from meya.tile.spec import TileElementSpec
from meya.tile.spec import TileEventSpec
from meya.tile.spec import TileLayout
from meya.user.meta_tag import UserInputTag
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class TileAskComponent(InteractiveComponent):
    """
    Show customizable tiles to the user.
    """

    meta_name: str = meta_field(value="Tiles")
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[UserInputTag, BotOutputTag]
    )

    ask: Optional[str] = element_field(default=None)
    tiles: List[TileElementSpec] = element_field(signature=True)
    button_style: Optional[TileButtonStyle] = element_field(default=None)
    layout: Optional[TileLayout] = element_field(default=None)
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )

    async def start(self) -> List[Entry]:
        tiles, triggers = TileEventSpec.from_element_spec_list(self.tiles)

        ask_tiles_event = TileAskEvent(
            button_style=self.button_style,
            layout=self.layout,
            text=self.ask,
            tiles=tiles,
        )

        return self.respond(ask_tiles_event, *triggers)
