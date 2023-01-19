from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonEventSpec
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.icon.spec import IconElementSpecUnion
from meya.tile.event.rating import RatingEvent
from meya.user.meta_tag import UserInputTag
from numbers import Real
from typing import List
from typing import Optional
from typing import Type


@dataclass
class Option:
    icon: Optional[IconElementSpecUnion] = None
    text: Optional[str] = None
    score: Optional[Real] = None

    @property
    def button_spec(self) -> ButtonElementSpec:
        return ButtonElementSpec(
            icon=self.icon, text=self.text, result=self.score
        )


class RatingIcons:
    # face icons"
    OPTION_0_FACE_ICON = (
        "streamline-regular/21-messages-chat-smileys/05-smileys/smiley-mad.svg"
    )
    OPTION_1_FACE_ICON = "streamline-regular/21-messages-chat-smileys/05-smileys/smiley-disapointed-mad.svg"
    OPTION_2_FACE_ICON = "streamline-regular/21-messages-chat-smileys/05-smileys/smiley-indifferent.svg"
    OPTION_3_FACE_ICON = "streamline-regular/21-messages-chat-smileys/05-smileys/smiley-smile-2.svg"
    OPTION_4_FACE_ICON = "streamline-regular/21-messages-chat-smileys/05-smileys/smiley-shine-big-eyes.svg"

    OPTION_STAR_ICON = "streamline-regular/22-social-medias-rewards-rating/06-rating/rating-star.svg"

    OPTION_0_THUMB_ICON = "streamline-regular/22-social-medias-rewards-rating/04-likes/dislike-1.svg"
    OPTION_1_THUMB_ICON = "streamline-regular/22-social-medias-rewards-rating/04-likes/like-1.svg"


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


class RatingType(Enum):
    FACES = "faces"
    STARS = "stars"
    THUMBS = "thumbs"
    CUSTOM = "custom"

    @property
    def options(self) -> List[Option]:
        assert self != RatingType.CUSTOM
        return {
            RatingType.FACES: [
                Option(icon=RatingIcons.OPTION_0_FACE_ICON, score=-2),
                Option(icon=RatingIcons.OPTION_1_FACE_ICON, score=-1),
                Option(icon=RatingIcons.OPTION_2_FACE_ICON, score=0),
                Option(icon=RatingIcons.OPTION_3_FACE_ICON, score=1),
                Option(icon=RatingIcons.OPTION_4_FACE_ICON, score=2),
            ],
            RatingType.STARS: [
                Option(icon=RatingIcons.OPTION_STAR_ICON, score=x + 1)
                for x in range(5)
            ],
            RatingType.THUMBS: [
                Option(icon=RatingIcons.OPTION_0_THUMB_ICON, score=-1),
                Option(icon=RatingIcons.OPTION_1_THUMB_ICON, score=1),
            ],
        }[self]

    @property
    def fill(self) -> bool:
        return self in [self.STARS]

    @property
    def backfill(self) -> bool:
        return self in [self.STARS]


@dataclass
class RatingComponent(InteractiveComponent):
    meta_level: float = meta_field(value=MetaLevel.BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])

    rating: RatingType = element_field(
        signature=True,
        help=(
            "The rating card comes with a number of built-in rating types. "
            "The most commonly used one is `thumbs`, which display thumbs "
            "up & down icons. You can also define your own set of icons, and "
            "their associated results, by setting this to `custom`."
        ),
    )
    options: Optional[List[Option]] = element_field(
        default=None,
        help=(
            "If you've set the rating type to `custom`, then you need to "
            "specify a list of rating options. Each option takes an icon "
            "spec, text and a score."
        ),
    )
    fill: Optional[bool] = element_field(
        default=None,
        help=(
            "When this is set to `true` then the Orb Web SDK will fill the "
            "icon with a solid color. Note that this is currently only "
            "applicable to the Orb Web SDK."
        ),
    )
    backfill: Optional[bool] = element_field(
        default=None,
        help=(
            "When this is set to `true` the Orb Web/Mobile SDK will highlight "
            "all the icons up to and including the selected icon. Note that "
            "for the Orb Web SDK both `fill` and `backfill` need to be set "
            "to `true`."
        ),
    )
    title: str = element_field(
        help="A text string describing the purpose of the rating."
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help="Override the Orb composer for this component.",
    )

    def validate(self):
        super().validate()
        if self.rating == RatingType.CUSTOM and not self.options:
            raise self.validation_error(
                "`options` are required when `rating: custom`"
            )

    async def start(self) -> List[Entry]:
        if self.rating == RatingType.CUSTOM:
            options = self.options
        else:
            options = self.rating.options
        button_specs = [option.button_spec for option in options]
        buttons, triggers = ButtonEventSpec.from_element_spec_union_list(
            button_specs
        )

        rating_event = RatingEvent(
            title=self.title,
            fill=self.rating.fill if self.fill is None else self.fill,
            backfill=self.rating.backfill
            if self.backfill is None
            else self.backfill,
            options=buttons,
        )
        return self.respond(rating_event, *triggers)
