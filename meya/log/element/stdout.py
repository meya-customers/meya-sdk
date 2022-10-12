import random

from colored import attr
from colored import fg
from colored import stylize
from dataclasses import dataclass
from meya.element import Element
from meya.entry import Entry
from meya.log.element import LogElement
from meya.log.element import LogRef
from meya.log.entry.exception import LogExceptionEntry
from typing import ClassVar
from typing import List
from typing import Type

# styles
ARROW = f"{fg('green') + attr('bold')}→{attr('reset')}"
LOG_PREFIX = f"{ARROW} {fg('light_blue') + attr('bold')}LOG:{attr('reset')}"

ENTRY_ID_STYLE = fg("green")
ENTRY_TYPE_STYLE = fg("light_magenta")
DATA_STYLE = fg("light_gray")
EXCEPTION_STYLE = fg("yellow")


@dataclass
class StdoutLogElement(LogElement):
    async def accept_sensitive(self) -> bool:
        return await self.accept()

    async def process(self) -> List[Entry]:
        if isinstance(self.encrypted_entry, LogExceptionEntry):
            print(
                LOG_PREFIX,
                stylize(self.encrypted_entry.entry_id, ENTRY_ID_STYLE),
                self.get_entry_type_formatted(),
                stylize(self.encrypted_entry, DATA_STYLE),
            )
            print(
                stylize(
                    f"{self.encrypted_entry.exception_type}"
                    f'("{self.encrypted_entry.exception}")',
                    EXCEPTION_STYLE,
                )
            )
            for trace_line in self.encrypted_entry.stack_trace:
                print(stylize(" ".join(trace_line), EXCEPTION_STYLE))
        else:
            print(
                LOG_PREFIX,
                stylize(self.encrypted_entry.entry_id, ENTRY_ID_STYLE),
                self.get_entry_type_formatted(),
                stylize(self.encrypted_entry, DATA_STYLE),
            )
        return []

    def get_entry_type_formatted(self):
        txt = self.encrypted_entry.get_entry_type()
        txt_random = random.Random(txt + "_")
        n = txt_random.randint(0, 255)
        return stylize(txt.ljust(24, " "), fg(n))


class StdoutLogRef(LogRef):
    element_type: ClassVar[Type[Element]] = StdoutLogElement
