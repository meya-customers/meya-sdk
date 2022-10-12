from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import response_field
from meya.front.element.mixin.contact.handle import FrontHandleMixin


@dataclass
class FrontContactHandleCreateComponentResponse:
    ok: bool = response_field(sensitive=True)


@dataclass
class FrontContactHandleCreateComponent(BaseApiComponent, FrontHandleMixin):
    pass
