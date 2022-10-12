from dataclasses import dataclass
from meya.user.avatar_crop import AvatarCrop
from typing import Optional


@dataclass
class Avatar:
    image: Optional[str] = None
    crop: AvatarCrop = AvatarCrop.CIRCLE
    monogram: Optional[str] = None
