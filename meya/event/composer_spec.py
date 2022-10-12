from dataclasses import dataclass
from dataclasses import field
from meya.util.enum import SimpleEnum
from typing import Optional


class ComposerFocus(SimpleEnum):
    FILE = "file"
    IMAGE = "image"
    TEXT = "text"
    BLUR = "blur"


class ComposerVisibility(SimpleEnum):
    COLLAPSE = "collapse"
    HIDE = "hide"
    SHOW = "show"


@dataclass
class ComposerCommonSpec:
    focus: Optional[ComposerFocus] = field(default=None)
    placeholder: Optional[str] = field(default=None)
    collapse_placeholder: Optional[str] = field(default=None)
    visibility: Optional[ComposerVisibility] = field(default=None)


@dataclass
class ComposerElementSpec(ComposerCommonSpec):
    pass


@dataclass
class ComposerEventSpec(ComposerCommonSpec):
    @classmethod
    def from_element_spec(
        cls, composer: ComposerElementSpec
    ) -> "ComposerEventSpec":
        return cls(
            focus=composer.focus,
            placeholder=composer.placeholder,
            collapse_placeholder=composer.collapse_placeholder,
            visibility=composer.visibility,
        )

    def __or__(self, other: "ComposerEventSpec") -> "ComposerEventSpec":
        return ComposerEventSpec(
            focus=self.focus if self.focus is not None else other.focus,
            placeholder=self.placeholder
            if self.placeholder is not None
            else other.placeholder,
            collapse_placeholder=self.collapse_placeholder
            if self.collapse_placeholder is not None
            else other.collapse_placeholder,
            visibility=self.visibility
            if self.visibility is not None
            else other.visibility,
        )


class ComposerSpec(ComposerElementSpec):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            f"Use `ComposerElementSpec` instead of `ComposerSpec`",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)
