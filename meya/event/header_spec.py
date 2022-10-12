from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import ButtonElementSpecUnion
from meya.button.spec import ButtonEventSpec
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.trigger.entry.activate import TriggerActivateEntry
from numbers import Real
from typing import List
from typing import Optional
from typing import Union


@dataclass
class HeaderTitleCommonSpec:
    text: Optional[str] = field(default=None)


@dataclass
class HeaderTitleElementSpec(HeaderTitleCommonSpec):
    icon: Optional[IconElementSpecUnion] = field(default=None)


HeaderTitleElementSpecUnion = Union[HeaderTitleElementSpec, str, bool]


@dataclass
class HeaderTitleEventSpec(HeaderTitleCommonSpec):
    icon: Optional[IconEventSpec] = field(default=None)

    @classmethod
    def from_element_spec_union(
        cls, title: HeaderTitleElementSpecUnion
    ) -> "HeaderTitleEventSpec":
        if isinstance(title, str):
            return HeaderTitleEventSpec(text=title)
        elif isinstance(title, HeaderTitleElementSpec):
            return HeaderTitleEventSpec(
                text=title.text,
                icon=IconEventSpec.from_element_spec(title.icon),
            )
        else:
            return HeaderTitleEventSpec()


@dataclass
class HeaderProgressCommonSpec:
    value: Optional[Real] = field(default=None)
    show_percent: Optional[bool] = field(default=None)


@dataclass
class HeaderProgressElementSpec(HeaderProgressCommonSpec):
    pass


HeaderProgressElementSpecUnion = Union[HeaderProgressElementSpec, Real, bool]


@dataclass
class HeaderProgressEventSpec(HeaderProgressCommonSpec):
    @classmethod
    def from_element_spec_union(
        cls, progress: HeaderProgressElementSpecUnion
    ) -> "HeaderProgressEventSpec":
        if isinstance(progress, Real):
            return HeaderProgressEventSpec(value=progress)
        elif isinstance(progress, HeaderProgressElementSpec):
            return HeaderProgressEventSpec(
                value=progress.value, show_percent=progress.show_percent
            )
        else:
            return HeaderProgressEventSpec()


@dataclass
class HeaderMilestoneCommonSpec:
    text: Optional[str] = field(default=None)
    current: bool = field(default=False)


@dataclass
class HeaderMilestoneElementSpec(HeaderMilestoneCommonSpec):
    pass


HeaderMilestoneElementSpecUnion = Union[HeaderMilestoneElementSpec, str, bool]


@dataclass
class HeaderMilestoneEventSpec(HeaderMilestoneCommonSpec):
    @classmethod
    def from_element_spec_union_list(
        cls, milestones: List[HeaderMilestoneElementSpecUnion]
    ) -> List["HeaderMilestoneEventSpec"]:
        return [
            cls.from_element_spec_union(milestone) for milestone in milestones
        ]

    @classmethod
    def from_element_spec_union(
        cls, milestone: HeaderMilestoneElementSpecUnion
    ) -> "HeaderMilestoneEventSpec":
        if isinstance(milestone, str):
            return HeaderMilestoneEventSpec(text=milestone)
        elif isinstance(milestone, bool):
            return HeaderMilestoneEventSpec(current=milestone)
        else:
            return HeaderMilestoneEventSpec(
                text=milestone.text, current=milestone.current
            )


@dataclass
class HeaderCommonSpec:
    pass


@dataclass
class HeaderElementSpec(HeaderCommonSpec):
    buttons: Optional[List[ButtonElementSpecUnion]] = field(default=None)
    title: Optional[HeaderTitleElementSpecUnion] = field(default=None)
    progress: Optional[HeaderProgressElementSpecUnion] = field(default=None)
    milestones: Optional[List[HeaderMilestoneElementSpecUnion]] = field(
        default=None
    )
    extra_buttons: Optional[List[ButtonElementSpecUnion]] = field(default=None)


@dataclass
class HeaderEventSpec(HeaderCommonSpec):
    buttons: Optional[List[ButtonEventSpec]] = field(default=None)
    title: Optional[HeaderTitleEventSpec] = field(default=None)
    progress: Optional[HeaderProgressEventSpec] = field(default=None)
    milestones: Optional[List[HeaderMilestoneEventSpec]] = field(default=None)
    extra_buttons: Optional[List[ButtonEventSpec]] = field(default=None)

    @classmethod
    def from_element_spec(
        cls, header: HeaderElementSpec, skip_triggers: bool = False
    ) -> ("HeaderEventSpec", List[TriggerActivateEntry]):
        buttons, button_triggers = (
            (None, [])
            if header.buttons is None
            else ButtonEventSpec.from_element_spec_union_list(
                header.buttons, skip_triggers=skip_triggers
            )
        )
        title = (
            None
            if header.title is None
            else HeaderTitleEventSpec.from_element_spec_union(header.title)
        )
        progress = (
            None
            if header.progress is None
            else HeaderProgressEventSpec.from_element_spec_union(
                header.progress
            )
        )
        milestones = (
            None
            if header.milestones is None
            else HeaderMilestoneEventSpec.from_element_spec_union_list(
                header.milestones
            )
        )
        extra_buttons, extra_button_triggers = (
            (None, [])
            if header.extra_buttons is None
            else ButtonEventSpec.from_element_spec_union_list(
                header.extra_buttons, skip_triggers=skip_triggers
            )
        )
        return (
            HeaderEventSpec(
                buttons=buttons,
                title=title,
                progress=progress,
                milestones=milestones,
                extra_buttons=extra_buttons,
            ),
            [*button_triggers, *extra_button_triggers],
        )

    def __or__(self, other: "HeaderEventSpec") -> "HeaderEventSpec":
        return HeaderEventSpec(
            buttons=self.buttons
            if self.buttons is not None
            else other.buttons,
            title=self.title if self.title is not None else other.title,
            progress=self.progress
            if self.progress is not None
            else other.progress,
            milestones=self.milestones
            if self.milestones is not None
            else other.milestones,
            extra_buttons=self.extra_buttons
            if self.extra_buttons is not None
            else other.extra_buttons,
        )
