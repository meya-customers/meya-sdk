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
    Show a set of tile cards that the user can scroll horizontally or
    vertically. Tiles are a great way to present rich data to the user and
    optionally get button click responses.

    Here is a basic example:

    ```yaml
    - tiles:
      - title: Super Nintendo Entertainment System
        description: 100,000 points
        image:
          url: https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/SNES-Mod1-Console-Set.jpg/800px-SNES-Mod1-Console-Set.jpg
        buttons:
          - text: Order
            result: nintendo
      - title: Sega Genesis
        description: 75,000 points
        image:
          url: https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Sega-Genesis-Mk2-6button.jpg/800px-Sega-Genesis-Mk2-6button.jpg
        buttons:
          - text: Order
            result: sega
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-ask-1.png" width="400"/>

    The ask tiles component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer)
    and set context data.

    Here is a more advanced example:

    ```yaml
    - tiles:
        - image:
            url: https://cataas.com/cat/says/Tile%200
          title: Title 0
          rows:
            -   - cell: How
                  value: harvesting
                - cell: A
                  value: clouds
            -   - cell: Away
                  value: far
                - cell: Harvesting
                  value: ship
          buttons:
            - url: https://cataas.com/cat/says/Link%20button%203
              text: Link button 3
            - url: https://cataas.com/cat/says/Link%20button%204
              text: Link button 4
            - text: Button 5
              result: 5
            - text: Button 6
              result: 6
          description: |
            Circumnavigated how far away ship of the imagination star stuff
            harvesting **star light** great turbulent clouds a billion trillion
        - image:
            url: https://cataas.com/cat/says/Tile%201
          title: Title 1
          rows:
            -   - cell: Stuff
                  value: trillion
                - cell: Light
                  value: circumnavigated
            -   - cell: How
                  value: of
                - cell: Harvesting
                  value: billion
          buttons:
            - url: https://cataas.com/cat/says/Link%20button%207
              text: Link button 7
            - url: https://cataas.com/cat/says/Link%20button%208
              text: Link button 8
            - text: Button 9
              result: 9
            - text: Button 10
              result: 10
          description: |
            Circumnavigated how far away ship of the imagination star stuff
            harvesting **star light** great turbulent clouds a billion trillion
        - image:
            url: https://cataas.com/cat/says/Tile%202
          title: Title 2
          rows:
            -   - cell: Circumnavigated
                  value: great
                - cell: Imagination
                  value: ship
            -   - cell: Turbulent
                  value: of
                - cell: Turbulent
                  value: light
          buttons:
            - url: https://cataas.com/cat/says/Link%20button%2011
              text: Link button 11
              context: {}
            - url: https://cataas.com/cat/says/Link%20button%2012
              text: Link button 12
            - text: Button 13
              result: 13
            - text: Button 14
              result: 14
          description: |
            Circumnavigated how far away ship of the imagination star stuff
            harvesting **star light** great turbulent clouds a billion trillion
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-ask-2.png" width="400"/>

    ### Column layout
    The tiles can also be displayed as a column of tiles instead of a row of
    tiles.

    Here is an example:

    ```yaml
    - layout: column
      tiles:
      - title: Super Nintendo Entertainment System
        description: 100,000 points
        image:
          url: https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/SNES-Mod1-Console-Set.jpg/800px-SNES-Mod1-Console-Set.jpg
        buttons:
          - text: Order
            result: nintendo
          - text: More into
      - title: Sega Genesis
        description: 75,000 points
        buttons:
          - text: Order
            result: sega
          - text: More into
      - title: Sony Playstation
        description: 200,000 points
        buttons:
          - text: Order
            result: sega
          - text: More into
    ```

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-ask-3.png" width="400"/>

    ### Button tiles
    The [`TileElementSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/tile/spec.py) also inherits from the
    [`AbstractButtonElementSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/button/spec.py) which means that each
    file can also become a button in itself.

    A tile will become a button when one of the `AbstractButtonElementSpec` fields
    are set.

    This can be useful if you would like the user to simply select the entire
    tile instead of a button with in the tile. Here is an example of three tiles that behave as buttons:

    ```yaml
    - tiles:
      - title: Super Nintendo Entertainment System
        description: 100,000 points
        result: nintendo
      - title: Sega Genesis
        description: 75,000 points
        result: sega
      - title: Sony Playstation
        description: 200,000 points
        result: sony
    ```

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-ask-4.png" width="400"/>

    These tile buttons can also be displayed as a set of radio buttons:

    ```yaml
    - button_style: radio
      tiles:
      - title: Super Nintendo Entertainment System
        description: 100,000 points
        result: nintendo
      - title: Sega Genesis
        description: 75,000 points
        result: sega
      - title: Sony Playstation
        description: 200,000 points
        result: sony
    ```

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-ask-5.png" width="400"/>
    """

    meta_name: str = meta_field(value="Tiles")
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[UserInputTag, BotOutputTag]
    )

    ask: Optional[str] = element_field(
        default=None, help="Question to send to the user."
    )
    tiles: List[TileElementSpec] = element_field(
        signature=True,
        help=(
            "The tile spec that allows you to control the how each tile should"
            "present data. Check the [`TileElementSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/tile/spec.py) "
            "Python class to see what each field does."
        ),
    )
    button_style: Optional[TileButtonStyle] = element_field(
        default=None,
        help=(
            "Define how the tile's buttons should work. It can be one of "
            "`action`, `radio`, or `text`. The default is `action`."
        ),
    )
    layout: Optional[TileLayout] = element_field(
        default=None,
        help=(
            "Define how the tiles should be rendered, either `column` or "
            "`row`. The default is `column`."
        ),
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help=(
            "The composer spec that allows you to control the Orb's input "
            "composer. Check the "
            "[Composer](https://docs.meya.ai/docs/composer) guide for more "
            "info."
        ),
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
