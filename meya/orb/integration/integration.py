from dataclasses import dataclass
from datetime import timedelta
from meya.data_collection.collect import CollectionScope
from meya.data_collection.collect import ContextData
from meya.data_collection.collect import IpAddressData
from meya.data_collection.collect import LanguageData
from meya.data_collection.collect import ReferrerData
from meya.data_collection.collect import UrlData
from meya.data_collection.location import LocationData
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.element.field import process_field
from meya.event.composer_spec import ComposerCommonSpec
from meya.event.composer_spec import ComposerElementSpec
from meya.event.composer_spec import ComposerEventSpec
from meya.event.entry import Event
from meya.event.header_spec import HeaderCommonSpec
from meya.event.header_spec import HeaderElementSpec
from meya.event.header_spec import HeaderEventSpec
from meya.http.entry.request import HttpRequestEntry
from meya.integration.element.element import FilterElementSpecUnion
from meya.integration.element.element import IntegrationFilter
from meya.integration.element.interactive import InteractiveIntegration
from meya.orb.entry.ws.publish_request import OrbWsPublishRequestEntry
from meya.thread.entry.data import ThreadDataEntry
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.enum import SimpleEnum
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class OrbThemeCommonSpec:
    brand_color: Optional[str] = None
    bot_avatar_monogram: Optional[str] = None
    bot_avatar_url: Optional[str] = None


@dataclass
class OrbThemeElementSpec(OrbThemeCommonSpec):
    pass


@dataclass
class OrbThemeConfigSpec(OrbThemeCommonSpec):
    @classmethod
    def from_element_spec(
        cls, theme: OrbThemeElementSpec
    ) -> "OrbThemeConfigSpec":
        return cls(
            brand_color=theme.brand_color,
            bot_avatar_monogram=theme.bot_avatar_monogram,
            bot_avatar_url=theme.bot_avatar_url,
        )


@dataclass
class ComposerUpload:
    progress_text: Optional[str] = None
    error_text: Optional[str] = None


@dataclass
class OrbComposerCommonSpec(ComposerCommonSpec):
    placeholder_text: Optional[str] = None
    collapse_placeholder_text: Optional[str] = None
    file_button_text: Optional[str] = None
    file_send_text: Optional[str] = None
    image_button_text: Optional[str] = None
    camera_button_text: Optional[str] = None
    gallery_button_text: Optional[str] = None
    upload: Optional[ComposerUpload] = None


@dataclass
class OrbComposerElementSpec(ComposerElementSpec, OrbComposerCommonSpec):
    pass


@dataclass
class OrbComposerConfigSpec(ComposerEventSpec, OrbComposerCommonSpec):
    @classmethod
    def from_element_spec(
        cls, composer: OrbComposerElementSpec
    ) -> "OrbComposerConfigSpec":
        base_result = super().from_element_spec(composer)
        return cls(
            focus=base_result.focus,
            placeholder=base_result.placeholder,
            collapse_placeholder=base_result.collapse_placeholder,
            visibility=base_result.visibility,
            character_limit=base_result.character_limit,
            placeholder_text=composer.placeholder_text,
            collapse_placeholder_text=composer.collapse_placeholder_text,
            file_button_text=composer.file_button_text,
            file_send_text=composer.file_send_text,
            image_button_text=composer.image_button_text,
            camera_button_text=composer.camera_button_text,
            gallery_button_text=composer.gallery_button_text,
            upload=composer.upload,
        )


@dataclass
class OrbHeaderCommonSpec(HeaderCommonSpec):
    pass


@dataclass
class OrbHeaderElementSpec(HeaderElementSpec, OrbHeaderCommonSpec):
    pass


@dataclass
class OrbHeaderConfigSpec(HeaderEventSpec, OrbHeaderCommonSpec):
    @classmethod
    def from_element_spec(
        cls, header: OrbHeaderElementSpec, skip_triggers: bool = False
    ) -> ("OrbHeaderConfigSpec", List[TriggerActivateEntry]):
        base_result, triggers = super().from_element_spec(
            header, skip_triggers=skip_triggers
        )
        return (
            OrbHeaderConfigSpec(
                buttons=base_result.buttons,
                title=base_result.title,
                progress=base_result.progress,
                milestones=base_result.milestones,
                extra_buttons=base_result.extra_buttons,
            ),
            triggers,
        )


@dataclass
class OrbMenuCommonSpec:
    close_text: Optional[str] = None
    back_text: Optional[str] = None


@dataclass
class OrbMenuElementSpec(OrbMenuCommonSpec):
    pass


@dataclass
class OrbMenuConfigSpec(OrbMenuCommonSpec):
    @classmethod
    def from_element_spec(
        cls, menu: OrbMenuElementSpec
    ) -> "OrbMenuConfigSpec":
        return cls(close_text=menu.close_text, back_text=menu.back_text)


@dataclass
class OrbDropCommonSpec:
    drag_and_drop_text: Optional[str] = None


@dataclass
class OrbDropElementSpec(OrbDropCommonSpec):
    pass


@dataclass
class OrbDropConfigSpec(OrbDropCommonSpec):
    @classmethod
    def from_element_spec(
        cls, drop: OrbDropElementSpec
    ) -> "OrbDropConfigSpec":
        return cls(drag_and_drop_text=drop.drag_and_drop_text)


@dataclass
class OrbSplashCommonSpec:
    ready_text: Optional[str] = None


@dataclass
class OrbSplashElementSpec(OrbSplashCommonSpec):
    pass


@dataclass
class OrbSplashConfigSpec(OrbSplashCommonSpec):
    @classmethod
    def from_element_spec(
        cls, splash: OrbSplashElementSpec
    ) -> "OrbSplashConfigSpec":
        return cls(ready_text=splash.ready_text)


class OrbLauncherType(SimpleEnum):
    ORB = "orb"
    MESSAGE = "message"
    HIDE = "hide"


@dataclass
class OrbLauncherCommonSpec:
    type: Optional[OrbLauncherType] = None
    icon: Optional[Union[str, bool]] = None
    text: Optional[Union[str, bool]] = None


@dataclass
class OrbLauncherElementSpec(OrbLauncherCommonSpec):
    pass


@dataclass
class OrbLauncherConfigSpec(OrbLauncherCommonSpec):
    @classmethod
    def from_element_spec(
        cls, launcher: OrbLauncherElementSpec
    ) -> "OrbLauncherConfigSpec":
        return cls(type=launcher.type, icon=launcher.icon, text=launcher.text)


@dataclass
class OrbMediaUploadCommonSpec:
    all: Optional[bool] = None
    file: Optional[bool] = None
    image: Optional[bool] = None


@dataclass
class OrbMediaUploadElementSpec(OrbMediaUploadCommonSpec):
    pass


@dataclass
class OrbMediaUploadConfigSpec(OrbMediaUploadCommonSpec):
    max_size: Optional[int] = None

    @classmethod
    def from_element_spec(
        cls, media_upload: OrbMediaUploadElementSpec
    ) -> "OrbMediaUploadConfigSpec":
        return cls(
            all=media_upload.all,
            file=media_upload.file,
            image=media_upload.image,
        )


# TODO: expand this set to be more accurate
DEFAULT_TX_GRIDQL = """
NOT (
    meya.http.event.webhook
    OR meya.csp.event.event
    OR meya.orb.event.device
    OR meya.orb.event.device.connect
    OR meya.orb.event.device.heartbeat
    OR meya.orb.event.device.state
)
"""


@dataclass
class OrbIntegrationFilter(IntegrationFilter):
    tx: FilterElementSpecUnion = element_field(default=DEFAULT_TX_GRIDQL)


@dataclass
class OrbCollectConfig:
    language: Optional[CollectionScope] = element_field(
        default=LanguageData.DEFAULT_SCOPE
    )
    ip_address: Optional[CollectionScope] = element_field(
        default=IpAddressData.DEFAULT_SCOPE
    )
    location: Optional[CollectionScope] = element_field(
        default=LocationData.DEFAULT_SCOPE
    )
    referrer: Optional[CollectionScope] = element_field(
        default=ReferrerData.DEFAULT_SCOPE
    )
    url: Optional[CollectionScope] = element_field(
        default=UrlData.DEFAULT_SCOPE
    )
    context: Optional[CollectionScope] = element_field(
        default=ContextData.DEFAULT_SCOPE
    )


@dataclass
class OrbIntegration(InteractiveIntegration):
    NAME: ClassVar[str] = "orb"
    show_get_status: ClassVar[bool] = False

    theme: OrbThemeElementSpec = element_field(
        default_factory=OrbThemeElementSpec,
        help=(
            "Allows you to set the Orb's theme properties such as the brand "
            "color, etc."
        ),
    )
    composer: OrbComposerElementSpec = element_field(
        default_factory=OrbComposerElementSpec,
        help=(
            "Allows you to set the Orb's composer properties such as "
            "placeholder, text, etc."
        ),
    )
    header: OrbHeaderElementSpec = element_field(
        default_factory=OrbHeaderElementSpec,
        help=(
            "Allows you to set the Orb's header properties such buttons, "
            "title, etc."
        ),
    )
    menu: OrbMenuElementSpec = element_field(
        default_factory=OrbMenuElementSpec,
        help=(
            "Allows you to set the Orb's menu properties such as "
            "close display text."
        ),
    )
    drop: OrbDropElementSpec = element_field(
        default_factory=OrbDropElementSpec,
        help=(
            "Allows you to set the Orb's drag and drop properties such as "
            "the drag and drop display text."
        ),
    )
    splash: OrbSplashElementSpec = element_field(
        default_factory=OrbSplashElementSpec,
        help=(
            "Allows you to the set the Orb Mobile SDK's splash screen "
            "properties. Note that this property is not fully observed yet, "
            "but will be in the future."
        ),
    )
    launcher: OrbLauncherElementSpec = element_field(
        default_factory=OrbLauncherElementSpec,
        help=(
            "Allows you to set the Orb's launcher properties such as the "
            "launcher type, text etc. Note that this is only applicable for "
            "the Orb Web SDK and not the Orb Mobile SDK."
        ),
    )
    media_upload: OrbMediaUploadElementSpec = element_field(
        default_factory=OrbMediaUploadElementSpec,
        help=(
            "Allows you to configure which media types are enabled for upload. "
            "If a specific type is not specified, the `all` value is used."
        ),
    )
    container: Optional[str] = element_field(
        default=None,
        help=(
            "The HTML container to mount the Orb in e.g. "
            '`document.querySelector("#orb-mount")`. Note that this is only '
            "applicable for the Orb Web SDK and not the Orb Mobile SDK."
        ),
    )
    session_expiry: timedelta = element_field(
        default=timedelta(days=30),
        help=(
            "The amount time until an Orb session expires. When the user "
            "connects after the session has expired, a new session will be "
            "created and the old session token will no longer be valid."
        ),
    )
    filter: IntegrationFilter = element_field(
        default_factory=OrbIntegrationFilter,
        help=(
            "This allows you to use GridQL to filter incoming and outgoing "
            "entries. This can be useful if you would like the Orb "
            "integration not to process a specific event, for example typing "
            "indicators or heartbeats."
        ),
    )
    collect: OrbCollectConfig = element_field(
        default_factory=OrbCollectConfig,
        help=(
            "The Orb integration collects a number data points, e.g. "
            "ip address, when a user connects. This property allows you to "
            "configure in which data scope (event|thread|user) each data "
            "point should be stored."
        ),
    )
    identity_verification: bool = element_field(
        default=True,
        help=(
            "Verify the identity of every Orb user. If disabled, the Orb user "
            "ID becomes self-authenticating, so it is recommended to use "
            "secure random user IDs (e.g. salted hash of app user ID or "
            "email)."
        ),
    )

    entry: Union[
        HttpRequestEntry, OrbWsPublishRequestEntry, ThreadDataEntry, Event
    ] = process_field()


class OrbIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = OrbIntegration
