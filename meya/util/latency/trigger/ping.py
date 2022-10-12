from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.text.trigger import TextTrigger
from meya.trigger.element import TriggerMatchResult


@dataclass
class PingTrigger(TextTrigger):
    extra_alias: str = meta_field(value="ping")

    keyword: str = element_field(default="_ping")

    async def match(self) -> TriggerMatchResult:
        [keyword, *options] = self.entry.text.split(" ")
        if keyword == self.keyword:
            ping_id = self.entry.entry_id
            benchmark = "benchmark" in options
            profile = "profile" in options
            # TODO Only allow profiling for staff users
            await self.latency_stats.start(ping_id, benchmark, profile)
            return self.succeed()
        else:
            return self.fail()
