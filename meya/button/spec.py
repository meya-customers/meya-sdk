import re

from abc import ABC
from abc import abstractmethod
from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import MISSING_FACTORY
from meya.util.enum import SimpleEnum
from meya.util.generate_id import generate_button_id
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


class ButtonType(SimpleEnum):
    # these do not have triggers
    TEXT = "text"
    URL = "url"
    STATIC = "static"
    MENU = "menu"
    DIVIDER = "divider"

    # these types can also have javascript
    ACTION = "action"
    FLOW_NEXT = "flow_next"
    COMPONENT_NEXT = "component_next"


_divider_pattern = re.compile(r"-{3,}")


@dataclass
class ButtonCommonSpec:
    url: Optional[str] = None
    javascript: Optional[str] = None
    button_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    default: Optional[bool] = None
    disabled: Optional[bool] = None
    divider: Optional[bool] = None


@dataclass
class AbstractButtonElementSpec(ButtonCommonSpec, ABC):
    icon: Optional[IconElementSpecUnion] = None
    action: Optional[ActionComponentSpec] = field(
        default=None,
        metadata=dict(
            help="Action executed if button clicked",
            level=MetaLevel.VERY_BASIC,
        ),
    )
    value: Any = field(default_factory=MISSING_FACTORY)
    result: Any = field(default_factory=MISSING_FACTORY)
    data: Optional[Dict[str, Any]] = None
    # can be specified explicitly or inferred
    magic: Optional[bool] = None
    type: Optional[ButtonType] = None
    menu: Optional[List["ButtonElementSpecUnion"]] = None

    @property
    @abstractmethod
    def text(self) -> Optional[str]:
        pass

    @property
    def flow_data(self) -> dict:
        if self.result is not MISSING:
            return dict(result=self.result)
        elif self.data is not None:
            return self.data
        else:
            return dict()

    @property
    def computed_magic(self) -> bool:
        return self.magic or (self.magic is None and self.default_magic)

    @property
    def default_magic(self) -> bool:
        return not any((self.url, self.icon, self.text))

    @property
    def computed_divider(self) -> bool:
        return bool(self.divider or _divider_pattern.match(self.text or ""))

    @property
    def computed_type(self) -> ButtonType:
        return self.type or self.default_type

    @property
    def default_type(self) -> ButtonType:
        if self.computed_divider:
            return ButtonType.DIVIDER
        elif self.url:
            return ButtonType.URL
        elif self.action:
            return ButtonType.ACTION
        elif self.result is not MISSING:
            return ButtonType.FLOW_NEXT
        elif self.data is not None:
            return ButtonType.FLOW_NEXT
        elif self.javascript:
            return ButtonType.STATIC
        elif self.button_id:
            return ButtonType.STATIC
        elif self.menu:
            return ButtonType.MENU
        else:
            return ButtonType.TEXT


@dataclass
class AbstractButtonEventSpec(ButtonCommonSpec, ABC):
    icon: Optional[IconEventSpec] = None
    menu: Optional[List["ButtonEventSpec"]] = None


@dataclass
class ButtonElementSpec(AbstractButtonElementSpec):
    text: Optional[str] = field(
        default=None,
        metadata=dict(help="Button text", level=MetaLevel.VERY_BASIC),
    )

    @staticmethod
    def get_snippet_default() -> str:
        return """
            text: Click me
            action: next
        """


ButtonElementSpecUnion = Union[ButtonElementSpec, str]


@dataclass
class ButtonEventSpec(AbstractButtonEventSpec):
    text: Optional[str] = None

    def to_transcript_text(self) -> str:
        if self.url:
            return f"--> [{self.text or '...'}] - {self.url}"

        return f"--> [{self.text or '...'}]"

    @classmethod
    def from_element_spec_union_list(
        cls, buttons: List[ButtonElementSpecUnion], skip_triggers: bool = False
    ) -> (List["ButtonEventSpec"], List[TriggerActivateEntry]):
        triggers = []
        button_results = []
        for button in buttons:
            new_button_result, new_triggers = cls.from_element_spec_union(
                button, skip_triggers=skip_triggers
            )
            button_results += [new_button_result] if new_button_result else []
            triggers += new_triggers
        return button_results, triggers

    @classmethod
    def from_element_spec_union(
        cls,
        button: Union[ButtonElementSpecUnion, AbstractButtonElementSpec],
        skip_triggers: bool = False,
    ) -> (Optional["ButtonEventSpec"], List[TriggerActivateEntry]):
        from meya.button.trigger import ButtonTrigger
        from meya.component.element.mixin import FlowControlMixin
        from meya.trigger.element import TriggerActionEntry

        if isinstance(button, str):
            button = ButtonElementSpec(text=button)

        if button.computed_type == ButtonType.TEXT:
            button_result = ButtonEventSpec(
                text=button.text,
                icon=IconEventSpec.from_element_spec(button.icon),
                context=button.context,
                default=button.default,
                disabled=button.disabled,
            )
            triggers = []

        elif button.computed_type == ButtonType.URL:
            button_result = ButtonEventSpec(
                text=button.text,
                icon=IconEventSpec.from_element_spec(button.icon),
                url=button.url if not button.disabled else None,
                context=button.context,
                default=button.default,
                disabled=button.disabled,
            )
            triggers = []

        elif button.computed_type == ButtonType.STATIC:
            button_result = ButtonEventSpec(
                text=button.text,
                icon=IconEventSpec.from_element_spec(button.icon),
                javascript=button.javascript,
                button_id=button.button_id or generate_button_id(),
                context=button.context,
                default=button.default,
                disabled=button.disabled,
            )
            triggers = []

        elif button.computed_type == ButtonType.MENU:
            (
                menu_button_results,
                menu_triggers,
            ) = cls.from_element_spec_union_list(button.menu)
            button_result = ButtonEventSpec(
                text=button.text,
                icon=IconEventSpec.from_element_spec(button.icon),
                menu=menu_button_results,
                context=button.context,
                default=button.default,
                disabled=button.disabled,
            )
            triggers = menu_triggers

        elif button.computed_type == ButtonType.DIVIDER:
            button_result = ButtonEventSpec(divider=True)
            triggers = []

        else:
            if button.computed_type == ButtonType.ACTION:
                [action_entry] = FlowControlMixin.flow_control_action(
                    button.action
                )

            elif button.computed_type == ButtonType.FLOW_NEXT:
                [action_entry] = FlowControlMixin.flow_control_next(
                    data=button.flow_data
                )

            elif button.computed_type == ButtonType.COMPONENT_NEXT:
                [action_entry] = FlowControlMixin.flow_control_component_next(
                    data=button.flow_data
                )

            else:
                raise NotImplementedError()

            disabled = True if skip_triggers else button.disabled
            button_id = (
                None if disabled else button.button_id or generate_button_id()
            )
            button_result = ButtonEventSpec(
                text=button.text,
                icon=IconEventSpec.from_element_spec(button.icon),
                button_id=button_id,
                context=button.context,
                default=button.default,
                disabled=disabled,
            )
            if button.javascript and not disabled:
                button_result.javascript = button.javascript

            triggers = (
                []
                if disabled
                else [
                    ButtonTrigger(
                        button_id=button_id,
                        action=TriggerActionEntry(
                            action_entry.to_typed_dict()
                        ),
                        text=button.text,
                    ).activate()
                ]
            )

        if button.computed_magic:
            button_result = None

        return button_result, triggers


@dataclass
class ButtonResultList:
    triggers: List[TriggerActivateEntry]
    buttons: List[ButtonEventSpec]


# TODO: Deprecate
ButtonSpecUnion = ButtonElementSpecUnion


class ButtonSpec(ButtonElementSpec):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            f"Use `ButtonElementSpec` instead of `ButtonSpec`",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)
