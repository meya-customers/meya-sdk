from meya.element import Element
from meya.element.field import element_field
from meya.element.field import meta_field
from typing import Optional


class IgnorecaseMixin(Element):
    is_abstract: bool = meta_field(value=True)

    ignorecase: Optional[bool] = element_field(default=None)

    @property
    def ignorecase_default_true(self):
        if self.ignorecase is None:
            return True
        else:
            return self.ignorecase
