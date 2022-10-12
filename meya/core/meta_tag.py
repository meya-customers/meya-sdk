from dataclasses import dataclass
from meya.icon.spec import IconElementSpecUnion
from meya.util.dict import dataclass_get_meta_value
from meya.util.dict import dataclass_get_own_meta_value
from typing import Optional


@dataclass
class MetaTag:
    @classmethod
    def get_meta_name(cls) -> Optional[str]:
        return dataclass_get_own_meta_value(cls, "meta_name")

    @classmethod
    def get_meta_icon(cls) -> IconElementSpecUnion:
        return (
            dataclass_get_meta_value(cls, "meta_icon")
            or "streamline-regular/05-internet-networks-servers/09-cloud/cloud-settings.svg"
        )

    @classmethod
    def get_meta_level(cls) -> Optional[float]:
        return dataclass_get_own_meta_value(cls, "meta_level")
