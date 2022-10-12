import re

from dataclasses import dataclass
from meya import env
from typing import Optional
from typing import Union


@dataclass
class IconCommonSpec:
    url: Optional[str] = None
    color: Optional[str] = None


@dataclass
class IconElementSpec(IconCommonSpec):
    path: Optional[str] = None

    @property
    def clean_path(self):
        return re.sub(r"\s&\s|[:\s]", "-", self.path)


IconElementSpecUnion = Union[IconElementSpec, str]


@dataclass
class IconEventSpec(IconCommonSpec):
    @classmethod
    def from_element_spec(
        cls, icon: Optional[IconElementSpecUnion]
    ) -> Optional["IconEventSpec"]:
        if icon is None:
            return None

        if isinstance(icon, str):
            icon = IconElementSpec(path=icon)

        if icon.path:
            icon = IconElementSpec(
                url=f"{env.cdn_url}/icon/{icon.clean_path}", color=icon.color
            )

        return cls(url=icon.url, color=icon.color)


# TODO: Deprecate
IconSpecUnion = IconElementSpecUnion


class IconSpec(IconElementSpec):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            f"Use `IconElementSpec` instead of `IconSpec`", DeprecationWarning
        )
        super().__init__(*args, **kwargs)
