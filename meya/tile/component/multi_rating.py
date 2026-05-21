from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import ButtonEventSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.tile.component.rating import Option
from meya.tile.component.rating import RatingType
from meya.tile.event.multi_rating import MultiRatingInputEvent
from meya.tile.event.multi_rating import RatingGroupEventSpec
from meya.user.meta_tag import UserInputTag
from meya.widget.component import WidgetInputValidationError
from meya.widget.component.component import WidgetMode
from meya.widget.component.field import FieldComponent
from typing import Any
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class MultiRatingSubmitButtonElementSpec:
    text: str = "Submit"


@dataclass
class RatingGroupElementSpec:
    title: str = field(
        metadata=dict(
            help="Text describing the purpose of this rating.",
            level=MetaLevel.VERY_BASIC,
        )
    )
    rating: RatingType = field(
        default=RatingType.STARS,
        metadata=dict(
            help="The rating type: faces, stars, thumbs, or custom.",
            level=MetaLevel.VERY_BASIC,
        ),
    )
    options: Optional[List[Option]] = field(
        default=None,
        metadata=dict(
            help="Custom options (required when rating: custom).",
            level=MetaLevel.BASIC,
        ),
    )
    fill: Optional[bool] = field(
        default=None,
        metadata=dict(
            help="Fill icons with solid color.",
            level=MetaLevel.INTERMEDIATE,
        ),
    )
    backfill: Optional[bool] = field(
        default=None,
        metadata=dict(
            help="Highlight all icons up to selection.",
            level=MetaLevel.INTERMEDIATE,
        ),
    )


@dataclass
class MultiRatingComponent(FieldComponent):
    """
    Collect multiple ratings in a single block. Each group displays a
    title and a set of rating icons. The user selects one option per
    group and submits all selections at once.

    ```yaml
    - type: meya.tile.component.multi_rating
      label: Please rate your experience
      required: true
      groups:
        - title: Product quality
          rating: stars
        - title: Support experience
          rating: thumbs
    ```

    The result is a list of scores in group order, e.g. `[4, 1]`.

    This component is also a widget component that can be displayed as a
    field in a page.

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages)
    guide for more info on creating advanced form wizards for collecting
    user input.
    """

    meta_level: float = meta_field(value=MetaLevel.BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])

    @dataclass
    class Response(FieldComponent.Response):
        result: List = response_field(sensitive=True)

    groups: List[RatingGroupElementSpec] = element_field(
        signature=True,
        help="List of rating groups to display.",
    )
    submit: MultiRatingSubmitButtonElementSpec = element_field(
        default_factory=MultiRatingSubmitButtonElementSpec,
        help="Submit button configuration.",
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help="Override the Orb composer for this component.",
    )
    error_message: str = element_field(
        default="Please provide all ratings.",
        level=MetaLevel.INTERMEDIATE,
    )

    def validate(self):
        super().validate()
        if not self.groups:
            raise self.validation_error(
                "`groups` must contain at least one rating group"
            )
        for group in self.groups:
            if group.rating != RatingType.CUSTOM:
                continue
            if not group.options:
                raise self.validation_error(
                    "`options` are required when `rating: custom`"
                )
            for option in group.options:
                if option.score is None:
                    raise self.validation_error(
                        "`score` is required on every option when "
                        "`rating: custom` (None is reserved for "
                        "'not answered')"
                    )

    async def build(self) -> List[Entry]:
        group_event_specs = []
        for group in self.groups:
            if group.rating == RatingType.CUSTOM:
                options = group.options
            else:
                options = group.rating.options

            button_specs = [option.button_spec for option in options]
            buttons, _triggers = ButtonEventSpec.from_element_spec_union_list(
                button_specs, skip_triggers=True
            )
            for button, option in zip(buttons, options):
                button.result = option.score

            fill = group.rating.fill if group.fill is None else group.fill
            backfill = (
                group.rating.backfill
                if group.backfill is None
                else group.backfill
            )

            group_event_specs.append(
                RatingGroupEventSpec(
                    title=group.title,
                    fill=fill,
                    backfill=backfill,
                    options=buttons,
                )
            )

        event = MultiRatingInputEvent(
            groups=group_event_specs,
            submit_button_text=self.submit.text
            if self.mode == WidgetMode.STANDALONE
            else None,
        )
        return self.respond(event)

    async def validate_input_data(self) -> Any:
        assert isinstance(self.input_data, list)
        assert len(self.input_data) == len(self.groups)
        if self.required:
            if any(score is None for score in self.input_data):
                raise WidgetInputValidationError(self.error_message)
        for score, group in zip(self.input_data, self.groups):
            if score is None:
                continue
            if group.rating == RatingType.CUSTOM:
                allowed = {opt.score for opt in (group.options or [])}
            else:
                allowed = {opt.score for opt in group.rating.options}
            if score not in allowed:
                raise WidgetInputValidationError(self.error_message)
        return self.input_data
