from dataclasses import dataclass
from meya.form.event import FormEvent


@dataclass
class FormOkEvent(FormEvent):
    pass
