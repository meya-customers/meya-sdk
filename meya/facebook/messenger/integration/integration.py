from dataclasses import dataclass
from meya.csp.integration.integration import CspIntegration
from meya.data_collection.collect import CollectionScope
from meya.element.element import Element
from meya.element.element import Ref
from meya.element.field import element_field
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class FacebookMessengerCollectConfig:
    first_name: Optional[CollectionScope] = element_field(default=None)
    last_name: Optional[CollectionScope] = element_field(default=None)
    profile_pic: Optional[CollectionScope] = element_field(default=None)
    locale: Optional[CollectionScope] = element_field(default=None)
    timezone: Optional[CollectionScope] = element_field(default=None)
    gender: Optional[CollectionScope] = element_field(default=None)


@dataclass
class FacebookMessengerPageConfig:
    page_id: int = element_field(help="Facebook Page ID")
    access_token: str = element_field(
        help="Token generated for the app to access this page"
    )


@dataclass
class FacebookMessengerIntegration(CspIntegration):
    NAME: ClassVar[str] = "facebook_messenger"

    mark_incoming_as_read: bool = element_field(default=True)
    app_id: int = element_field(help="Facebook Messenger App ID")
    pages: List[FacebookMessengerPageConfig] = element_field(
        help="Pages connected to the app"
    )
    collect: FacebookMessengerCollectConfig = element_field(
        default_factory=FacebookMessengerCollectConfig,
        help=(
            "Fields you want to retrieve from the user profile, "
            "e.g. first name, last name. For more information see "
            "https://developers.facebook.com/docs/messenger-platform/identity/user-profile."
            "This property also allows you to configure in which data scope "
            "(event|thread|user) each data point should be stored."
        ),
    )


class FacebookMessengerIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = FacebookMessengerIntegration
