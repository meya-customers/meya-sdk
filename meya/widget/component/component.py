from dataclasses import MISSING
from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element import Element
from meya.element import Spec
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.util.enum import SimpleEnum
from meya.widget.event.event import WidgetEvent
from typing import Any
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type


class WidgetMode(SimpleEnum):
    STANDALONE = "standalone"
    PAGE = "page"


@dataclass
class WidgetInputValidationResult:
    validated_data: Any
    error: Optional[str]
    ok: bool


class WidgetInputValidationError(Exception):
    pass


@dataclass
class WidgetComponent(InteractiveComponent):
    """
    This is an abstract component and is used by the following components:

    - [button.ask](https://docs.meya.ai/reference/meya-button-component-ask)
    - [file.v2](https://docs.meya.ai/reference/meya-file-component-v2)
    - [image.v2](https://docs.meya.ai/reference/meya-image-component-v2)
    - [text.info](https://docs.meya.ai/reference/meya-text-component-info)
    - [widget.field](https://docs.meya.ai/reference/meya-widget-component-field)
    - [widget.page](https://docs.meya.ai/reference/meya-widget-component-page)

    **Note**, this component is only compatible with the
    [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk)
    and [Meya Orb Mobile SDK](https://docs.meya.ai/docs/orb-mobile-sdk).
    """

    @dataclass
    class Response:
        result: Any = response_field(sensitive=True)

    is_abstract: bool = meta_field(value=True)
    mode: WidgetMode = process_field()
    input_data: Any = process_field()
    input_validation: WidgetInputValidationResult = process_field()

    def __post_init__(self):
        super().__post_init__()
        self.mode = MISSING
        self.input_data = MISSING
        self.input_validation = MISSING

    async def start(self) -> List[Entry]:
        entries = await self.get_build_result(
            WidgetMode.STANDALONE, input_data=None
        )
        return self.respond(*entries)

    async def get_build_result(
        self, mode: WidgetMode, input_data: Any, *, post_process: bool = False
    ) -> List[Entry]:
        self.mode = mode
        self.input_data = input_data
        self.input_validation = await self.get_input_validation_result()
        entries = await self.build()
        self.respond_data = MISSING
        if post_process:
            entries = self.post_process_all(entries)
        assert len(entries) >= 1
        assert isinstance(entries[0], WidgetEvent)
        return entries

    async def get_input_validation_result(self) -> WidgetInputValidationResult:
        if self.input_data is None:
            validated_data = None
            error = None
        else:
            try:
                validated_data = await self.validate_input_data()
                error = None
            except WidgetInputValidationError as e:
                validated_data = None
                error = str(e)
            except AssertionError:
                self.log.exception()
                validated_data = None
                error = "Invalid input data"
        ok = self.input_data is not None and not error
        return WidgetInputValidationResult(
            validated_data=validated_data, error=error, ok=ok
        )

    async def validate_input_data(self) -> Any:
        """Override to accept input data"""
        assert False

    async def build(self) -> List[Entry]:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")


@dataclass
class WidgetComponentSpec(Spec):
    element_type: ClassVar[Type[Element]] = WidgetComponent

    snippet_default: str = meta_field(value="type: text_input")
