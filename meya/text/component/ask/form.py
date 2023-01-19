from dataclasses import dataclass
from dataclasses import field
from meya.component.element import ComponentOkResponse
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.util.generate_id import generate_form_id
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class AskFormComponent(InteractiveComponent):
    """
    Get basic text input from the user using a form text input. Normally the
    user will use the composer to input text, but this component allows you
    to specify additional meta information such as an **icon**, **label**,
    **placeholder**.

    ```yaml
    - ask_form: What is your name?
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-ask-form.png" width="400"/>

    Notice that the input form's label says **TEXT**, this is the default value,
    but usually you would like to customize this to be more descriptive. Here is
    an example of customizing the form text input:

    ```yaml
    - ask_form: What is your name?
      label: Name
      icon: streamline-regular/17-users/10-geomertic-close-up-single-user-neutral/single-neutral.svg
      placeholder: Type your name here
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-ask-form-1.png" width="400"/>

    **Note**, this component is only compatible with the
    [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk)
    and [Meya Orb Mobile SDK](https://docs.meya.ai/docs/orb-mobile-sdk).

    The ask form component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown),
    set context data and attach [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is a more advanced example:

    ```yaml
    - ask_form: What is your **name**? [What's in a name...](https://en.wikipedia.org/wiki/Name)
      label: Name
      icon: streamline-regular/17-users/10-geomertic-close-up-single-user-neutral/single-neutral.svg
      placeholder: Type your name here
      quick_replies:
        - text: Discover earth
          action:
            flow: flow.earth
        - text: Talk to an agent
          action:
            flow: flow.agent
      context:
        foo: bar
      composer:
        focus: text
        placeholder: Type your name here
      markdown:
        - format
        - linkify
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-ask-form-2.png" width="400"/>

    ### Input validation

    The ask component has no built-in input validation and will capture any
    text input submitted by the user.

    The user's input text is always stored in `(@ flow.result )` in your app's
    [flow scope](https://docs.meya.ai/docs/scope#flow) data.

    ### Advanced forms

    If you would like to build more complex form wizards, then checkout the
    [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide.
    """

    ask_form: Optional[str] = element_field(
        signature=True, default=None, help="Question sent to the user."
    )
    icon: Optional[IconElementSpecUnion] = element_field(
        default=None, help="Optional icon URL to user for the form input."
    )
    field_name: Optional[str] = element_field(
        default="text", help="The field name."
    )
    autocomplete: Optional[str] = element_field(
        default="off",
        help=(
            "Turns off browser autocomplete for the input form. This is only "
            "applicable for the Meya Orb Web SDK."
        ),
    )
    label: str = element_field(
        default="Text",
        help="The input form label displayed above the input form.",
    )
    placeholder: Optional[str] = element_field(
        default=None,
        help="The optional placeholder text displayed in the input form box.",
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help=(
            "The composer spec that allows you to control the Orb's input "
            "composer. Check the "
            "[Composer](https://docs.meya.ai/docs/composer) guide for more "
            "info."
        ),
    )

    async def start(self) -> List[Entry]:
        ask_form_event = FormAskEvent(
            form_id=generate_form_id(),
            fields=[
                Field(
                    name=self.field_name,
                    autocomplete=self.autocomplete,
                    icon=IconEventSpec.from_element_spec(self.icon),
                    placeholder=self.placeholder,
                    label=self.label,
                    required=True,
                    type=FieldType.TEXT,
                )
            ],
            text=self.ask_form,
        )
        return self.respond(
            ask_form_event, self.trigger(ask_form_event.form_id)
        )

    async def next(self) -> List[Entry]:
        encrypted_form_submit_event: FormSubmitEvent = Entry.from_typed_dict(
            self.entry.data["event"]
        )
        form_submit_event = await self.db.try_decrypt_sensitive_entry(
            encrypted_form_submit_event
        )
        input_result = ComponentOkResponse(
            result=form_submit_event.fields[self.field_name]
        )
        form_ok_event = FormOkEvent(form_id=form_submit_event.form_id)
        return self.respond(form_ok_event, data=input_result)

    def trigger(self, form_id: str):
        return FormTrigger(
            action=self.get_next_action(), form_id=form_id
        ).activate()
