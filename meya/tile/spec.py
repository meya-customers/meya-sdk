from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import AbstractButtonElementSpec
from meya.button.spec import AbstractButtonEventSpec
from meya.button.spec import ButtonElementSpecUnion
from meya.button.spec import ButtonEventSpec
from meya.core.meta_level import MetaLevel
from meya.icon.spec import IconEventSpec
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import MISSING_FACTORY
from meya.util.enum import SimpleEnum
from typing import Any
from typing import List
from typing import Optional
from typing import Union


@dataclass
class TileImage:
    url: str
    alt: Optional[str] = None


@dataclass
class TileCell:
    cell: str
    value: Any


@dataclass
class TileCommonSpec:
    title: Optional[str] = field(
        default=None,
        metadata=dict(help="Title for the tile", level=MetaLevel.VERY_BASIC),
    )
    description: Optional[str] = field(
        default=None,
        metadata=dict(help="Description for the tile", level=MetaLevel.BASIC),
    )
    image: Optional[TileImage] = field(
        default=None,
        metadata=dict(help="Image for the tile", level=MetaLevel.BASIC),
    )
    rows: List[List[TileCell]] = field(
        default_factory=list,
        metadata=dict(help="Rows of data for the tile", level=MetaLevel.BASIC),
    )


@dataclass
class TileElementSpec(AbstractButtonElementSpec, TileCommonSpec):
    buttons: List[ButtonElementSpecUnion] = field(
        default_factory=list,
        metadata=dict(
            snippet_default="""
                - text: Click me
                  action: next
            """,
            help="List of buttons shown on the tile",
            level=MetaLevel.BASIC,
        ),
    )

    @property
    def text(self) -> Optional[str]:
        return self.title or self.description

    @property
    def default_magic(self) -> bool:
        return not any(
            (
                self.title,
                self.description,
                self.icon,
                self.image,
                self.url,
                any(self.rows),
                any(
                    isinstance(button, str) or not button.computed_magic
                    for button in self.buttons
                ),
            )
        )

    @staticmethod
    def get_snippet_default() -> str:
        return """
            title: Title
            buttons:
              - text: Click me
                action: next
        """


@dataclass
class TileEventSpec(AbstractButtonEventSpec, TileCommonSpec):
    buttons: List[ButtonEventSpec] = field(default_factory=list)

    @classmethod
    def from_element_spec_list(
        cls, tiles: List[TileElementSpec], skip_triggers: bool = False
    ) -> (List["TileEventSpec"], List[TriggerActivateEntry]):
        triggers = []
        tile_results = []
        for tile in tiles:
            new_tile_result, new_triggers = cls.from_element_spec(
                tile, skip_triggers=skip_triggers
            )
            tile_results += [new_tile_result] if new_tile_result else []
            triggers += new_triggers
        return tile_results, triggers

    @classmethod
    def from_element_spec(
        cls, tile: TileElementSpec, skip_triggers: bool = False
    ) -> (Optional["TileEventSpec"], List[TriggerActivateEntry]):
        (
            tile_button,
            tile_button_triggers,
        ) = ButtonEventSpec.from_element_spec_union(
            tile, skip_triggers=skip_triggers
        )

        buttons, tile_triggers = ButtonEventSpec.from_element_spec_union_list(
            tile.buttons, skip_triggers=skip_triggers
        )

        if tile_button:
            tile_result = TileEventSpec(
                context=tile_button.context,
                button_id=tile_button.button_id,
                buttons=buttons,
                description=tile.description,
                icon=IconEventSpec.from_element_spec(tile.icon),
                image=tile.image,
                javascript=tile_button.javascript,
                rows=tile.rows,
                title=tile.title,
                url=tile_button.url,
                default=tile_button.default,
                disabled=tile_button.divider,
                menu=tile_button.menu,
            )
        else:
            tile_result = None

        return tile_result, [*tile_button_triggers, *tile_triggers]


class TileButtonStyle(SimpleEnum):
    ACTION = "action"
    RADIO = "radio"
    TEXT = "text"


class TileLayout(SimpleEnum):
    COLUMN = "column"
    ROW = "row"


class TileSpec(TileElementSpec):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            f"Use `TileElementSpec` instead of `TileSpec`", DeprecationWarning
        )
        super().__init__(*args, **kwargs)


@dataclass
class ChoiceCommonSpec:
    text: str = field(
        metadata=dict(help="Text for the choice", level=MetaLevel.VERY_BASIC)
    )
    default: Optional[bool] = field(default=None)
    disabled: Optional[bool] = field(default=None)


@dataclass
class ChoiceElementSpec(ChoiceCommonSpec):
    value: Any = field(default_factory=MISSING_FACTORY)

    @staticmethod
    def get_snippet_default() -> str:
        return """
            text: Pick this
        """


ChoiceElementSpecUnion = Union[ChoiceElementSpec, str]


@dataclass
class ChoiceEventSpec(ChoiceCommonSpec):
    pass
