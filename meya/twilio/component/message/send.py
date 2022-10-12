from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element import Element
from meya.element.field import element_field
from meya.twilio.integration import TwilioIntegration
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from typing import Optional
from typing import cast


@dataclass
class TwilioMessageSendComponent(BaseApiComponent):
    to: str = element_field()
    from_: Optional[str] = element_field(default=None)
    body: str = element_field()
    integration: TwilioBaseIntegrationRef = element_field()

    def validate(self):
        super().validate()
        if not self.from_:
            integration_spec = self.spec_registry.resolve(self.integration)
            if integration_spec.is_partial:
                # Skip validation for dynamic integration, let any runtime errors happen
                return

            integration = cast(
                TwilioIntegration, Element.from_spec(integration_spec)
            )
            if not integration.phone_number:
                raise self.validation_error(
                    f"`from` or `phone_number` required in {integration.id}"
                )
