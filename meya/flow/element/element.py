from dataclasses import dataclass
from meya.component.spec import FlowComponentSpec
from meya.core.base_ref import BaseRef
from meya.core.source_location import SourceLocation
from meya.element import AbstractSpecRegistry
from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element.element_error import ElementValidationError
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.flow.entry import FlowEntry
from meya.icon.spec import IconElementSpecUnion
from meya.trigger.element import FlowTriggerSpec
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type
from typing import Union
from typing import cast


@dataclass
class StepLabel:
    step_label: str


@dataclass
class Flow(Element):
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/41-hierachy-organization/hierarchy-2.svg"
    )

    triggers: List[FlowTriggerSpec] = element_field(default_factory=list)
    steps: List[Union[StepLabel, FlowComponentSpec]] = element_field(
        signature=True
    )

    entry: FlowEntry = process_field()

    def resolve_label(self, label: "StepLabelRef") -> int:
        return self._resolve_label(label)

    def try_resolve_label(self, label: "StepLabelRef") -> Optional[int]:
        return self._resolve_label(label, None)

    def _resolve_label(self, label: "StepLabelRef", *default):
        use_implicit_start_fallback = label.ref == "start" and (
            len(self.steps) == 0 or not isinstance(self.steps[0], StepLabel)
        )
        return next(
            (
                i
                for i, label_or_step in enumerate(self.steps)
                if isinstance(label_or_step, StepLabel)
                and label_or_step.step_label == label.ref
            ),
            *((0,) if use_implicit_start_fallback else default),
        )


class FlowSpec(Spec):
    element_type: ClassVar[Type[Element]] = Flow


class FlowRef(Ref):
    element_type: ClassVar[Type[Element]] = Flow


class StepLabelRef(BaseRef):
    def validate(
        self, flow_ref: FlowRef, source_location: Optional[SourceLocation]
    ):
        flow_spec = AbstractSpecRegistry.current.get().resolve(flow_ref)
        if flow_spec.is_partial:
            # Skip validation for dynamic flows, let any runtime errors happen
            return

        flow = cast(Flow, Element.from_spec(flow_spec))
        if flow.try_resolve_label(self) is None:
            raise ElementValidationError(
                source_location,
                f'flow "{flow.id}" does not have a ({self}) label',
            )
