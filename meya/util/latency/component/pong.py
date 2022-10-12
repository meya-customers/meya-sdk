from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event.composer_spec import ComposerEventSpec
from meya.file.event import FileEvent
from meya.icon.spec import IconEventSpec
from meya.text.event.say import SayEvent
from meya.util.json import to_json
from meya.util.latency.trigger.ping import PingTrigger
from typing import List

PROFILE_URL_SUFFIX = "_profile_blob_url"
PROFILE_ICON = "streamline-regular/07-work-office-companies/07-office-files/office-file-text-graph.svg"


@dataclass
class PongComponent(InteractiveComponent):
    extra_alias: str = meta_field(value="pong")

    keyword: str = element_field(default="_pong")

    async def start(self) -> List[Entry]:
        ping_event: SayEvent = Entry.from_typed_dict(
            self.entry.data[PingTrigger.EVENT_KEY]
        )
        latency_data = await self.latency_stats.end(ping_event.entry_id)
        self.log.info("Latency stats", latency_data)
        benchmark = latency_data.pop("benchmark")
        grid_profile_blob_url = latency_data.pop("grid_profile_blob_url", None)
        app_profile_blob_url = latency_data.pop("app_profile_blob_url", None)

        if benchmark:
            output = f"{self.keyword} {to_json(latency_data, pretty=True)}"
        else:
            output = f"{self.keyword} {latency_data['internal']:0.1f}ms"

        say_event = SayEvent(text=output)
        profile_events = [
            self._make_profile_file(
                latency_data["ping"], grid_profile_blob_url, "grid"
            ),
            self._make_profile_file(
                latency_data["ping"], app_profile_blob_url, "app"
            ),
        ]
        return self.respond(say_event, *filter(bool, profile_events))

    def _make_profile_file(self, ping, blob_url, prefix):
        if not blob_url:
            return None

        filename = f"{prefix}_{ping}.prof"
        return FileEvent(
            composer=ComposerEventSpec.from_element_spec(self.composer),
            filename=filename,
            icon=IconEventSpec.from_element_spec(PROFILE_ICON),
            url=f"{blob_url}?download={filename}",
        )
