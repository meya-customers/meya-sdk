from dataclasses import dataclass
from meya import env
from meya.data_collection.collect import CollectionScope
from meya.data_collection.collect import ContextData
from meya.data_collection.collect import IpAddressData
from meya.data_collection.collect import LanguageData
from meya.data_collection.collect import ReferrerData
from meya.data_collection.collect import UrlData
from meya.data_collection.location import LocationData
from meya.element.field import element_field
from meya.element.field import process_field
from meya.integration.element.interactive import InteractiveIntegration
from os import path
from typing import ClassVar
from typing import Optional


@dataclass
class WebV1CollectConfig:
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
class WebV1Integration(InteractiveIntegration):
    NAME: ClassVar[str] = "webv1"
    show_get_status: ClassVar[bool] = False

    suppress_echo: bool = process_field(default=False)
    collect: WebV1CollectConfig = element_field(
        default_factory=WebV1CollectConfig
    )

    @classmethod
    def get_gateway_webhook_url(
        cls, integration_id: str, app_id: Optional[str] = None
    ) -> str:
        return path.join(
            env.grid_url, "gateway", "v2", cls.NAME, integration_id
        )
