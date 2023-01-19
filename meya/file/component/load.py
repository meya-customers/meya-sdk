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
    Load a text file from your app's code repo and store it in
    `(@ flow.result )` in the [flow scope](https://docs.meya.ai/docs/scope#flow).

    You can also treat this text file as a template file that includes
    [Meya template](https://docs.meya.ai/docs/jinja2-syntax) tags that can
    be rendered using a template context dictionary.

    This component is particularly useful when you need to send HTML emails
    and would like to use an email template to standardize the email design.

    The following example will load the `templates/email.html` template file
    and render it using the Meya template syntax. The `template_context` gets
    made available to the template rendering engine so you would
    be able to reference the user's name using `(@ name )`.

    ```yaml
    steps:
      - file_path: templates/email.html
        template: true
        template_context:
          flow: (@ flow )
          name: (@ user.name )
          email: (@ user.email )
          foo: bar
    ```

    **template/email.html**
    ```html
    <html>
      <body>
        <p>
          Hi, (@ name )
        </p>
        <p>
            This is to notify you that your email address <b>(@ email )</b> has
            been changed to <b>(@ flow.new_email)</b>
        </p>
        <p>
            Thanks!
        </p>
      </body>
    </html>
    ```
    """

    run_in_app_container: bool = meta_field(value=True)

    file_path: str = element_field(
        signature=True,
        help="The file path relative to the app's root folder.",
    )
    template: bool = element_field(
        default=False,
        help="The file must be rendered using the Meya template syntax.",
    )
    template_context: Optional[Dict[str, Any]] = element_field(
        default=None, help="Optional context variables used in the template."
    )

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
