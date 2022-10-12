from dataclasses import dataclass
from dataclasses import field
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element.element import FilterElementSpecUnion
from meya.orb.integration import OrbIntegration
from meya.orb.integration.integration import OrbIntegrationFilter
from meya.util.enum import SimpleEnum
from numbers import Real
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class AndroidSpec:
    service_account_key: Union[str, dict]
    project_id: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    click_action: Optional[str] = field(default=None)
    custom_data: Optional[Dict[str, Any]] = field(default=None)


class IosApnsMode(SimpleEnum):
    DEV = "dev"
    PROD = "prod"


@dataclass
class IosSpec:
    auth_key: str = field()
    auth_key_id: str = field()
    team_id: str = field()
    topic: str = field()
    title: Optional[str] = field(default=None)
    sound: Optional[str] = field(default=None)
    title_loc_key: Optional[str] = field(default=None)
    title_loc_args: Optional[List[str]] = field(default=None)
    action_loc_key: Optional[str] = field(default=None)
    loc_key: Optional[str] = field(default=None)
    loc_args: Optional[List[str]] = field(default=None)
    launch_image: Optional[str] = field(default=None)
    apns_mode: IosApnsMode = field(default=IosApnsMode.DEV)
    custom_data: Optional[Dict[str, Any]] = field(default=None)


DEFAULT_PUSH_GRIDQL = """
NOT (
    meya.analytics.event.identify
    OR meya.session.event.chat.close
    OR meya.session.event.chat.open
    OR meya.session.event.page.open
    OR meya.orb.event.screen.continue
    OR meya.orb.event.screen.end
    OR meya.analytics.event.track
    OR meya.presence.event.typing
    OR meya.presence.event.typing.on
    OR meya.presence.event.typing.off
    OR meya.orb.event.device
    OR meya.orb.event.device.connect
    OR meya.orb.event.device.heartbeat
    OR meya.orb.event.device.state
)
"""


@dataclass
class OrbMobileIntegrationFilter(OrbIntegrationFilter):
    push_tx: FilterElementSpecUnion = element_field(
        default=DEFAULT_PUSH_GRIDQL,
        help=(
            "A GridQL query that will be applied to all TX events when a "
            "user's devices is in an in-active state. Note, that this filter "
            "is applied in addition to the standard `filter.tx` filter "
            "for the integration."
        ),
    )


@dataclass
class OrbMobileIntegration(OrbIntegration):
    NAME: ClassVar[str] = "orb_mobile"

    heartbeat_interval_seconds: Optional[Real] = element_field(
        default=30,
        help=(
            "The period at which the Orb Mobile SDK will send a hearbeat to "
            "indicate that the device's connection is active. If you set "
            "this property to `null` then the Orb Mobile SDK will not send "
            "any heartbeats and push notifications will only use the reported "
            "device state to determine whether or not to send a push "
            "notification."
        ),
    )
    inactive_timeout_seconds: Real = element_field(
        default=35,
        help=(
            "The number of seconds from the last active heartbeat to wait "
            "before marking the connection as inactive. Note that this must "
            "always be greater than `heartbeat_interval_seconds`."
        ),
    )
    android: Optional[AndroidSpec] = element_field(
        default=None,
        help=(
            "This contains all the settings for push notifications on Android."
        ),
    )
    ios: Optional[IosSpec] = element_field(
        default=None,
        help=("This contains all the settings for push notifications on iOS."),
    )
    filter: OrbMobileIntegrationFilter = element_field(
        default_factory=OrbMobileIntegrationFilter
    )

    def validate(self):
        super().validate()
        if (
            self.heartbeat_interval_seconds
            and self.heartbeat_interval_seconds
            >= self.inactive_timeout_seconds
        ):
            raise self.validation_error(
                "the 'inactive_timeout_seconds' property must be greater than "
                "the 'heartbeat_interval_seconds' property"
            )


class OrbMobileIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = OrbMobileIntegration
