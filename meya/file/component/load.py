from dataclasses import dataclass
from meya.component.element import Component
from meya.core.context import create_render_context
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.util.template import from_template_async
from meya.util.template import to_template_async
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class FileLoadComponent(Component):
    """
    file_path: relative file path from the app root including filename
    render: if True, renders using Meya's jinja2 templating
    context: dict used for jinja2 templating, if None defaults to app render context
    """

    run_in_app_container: bool = meta_field(value=True)

    file_path: str = element_field(signature=True)
    template: bool = element_field(default=False)
    template_context: Optional[Dict[str, Any]] = element_field(default=None)

    @dataclass
    class Response:
        result: str = response_field(sensitive=True)

    async def start(self) -> List[Entry]:
        with open(self.file_path, "r") as content_file:
            content = content_file.read()
        if self.template:
            context = self.template_context or await create_render_context()
            content = await from_template_async(
                context, to_template_async(content)
            )
        return self.respond(data=self.Response(result=content))
