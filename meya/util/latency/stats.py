import marshal

from contextlib import contextmanager
from cProfile import Profile
from dataclasses import dataclass
from dataclasses import field
from meya import env
from meya.time import get_milliseconds_perf_counter
from meya.time import get_milliseconds_process_time
from meya.util.context_var import ScopedContextVar
from meya.util.dict import to_dict
from typing import Callable
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Tuple
from typing import cast


@dataclass
class LatencyRun:
    ping_id: str
    ping_perf_counter: float
    ping_process_time: float
    benchmark: bool
    profile: Optional[Profile]
    render_list: List[Tuple[float, Optional[str], Optional[str]]]
    query_list: List[Tuple[float, str]]


@dataclass
class LatencyData:
    ping: str
    internal: float
    process_time: float
    benchmark: bool
    profile_blob_url: Optional[str]
    render_time: float
    render_list: List[Tuple[float, Optional[str], Optional[str]]]
    query_time: float
    query_list: List[Tuple[float, str]]


@dataclass
class LatencyStats:
    run: Optional[LatencyRun] = field(init=False, default=None)

    current: ClassVar = cast(
        ScopedContextVar["LatencyStats"], ScopedContextVar()
    )

    async def start(self, ping_id: str, benchmark: bool, profile: bool):
        if profile:
            profile_object = Profile()
            profile_object.enable()
        else:
            profile_object = None
        self.run = LatencyRun(
            ping_id=ping_id,
            ping_perf_counter=get_milliseconds_perf_counter(),
            ping_process_time=get_milliseconds_process_time(),
            benchmark=benchmark,
            profile=profile_object,
            render_list=list(),
            query_list=list(),
        )

    @contextmanager
    def _add_time(self, run_list: Callable[[], list], extra: Tuple):
        if not self.run:
            yield
            return

        perf_start = get_milliseconds_perf_counter()
        try:
            yield
        finally:
            perf_end = get_milliseconds_perf_counter()
            run_list().append((perf_end - perf_start, *extra))

    def add_render_time(
        self, spec_id: Optional[str], spec_type: Optional[str] = None
    ):
        return self._add_time(
            lambda: self.run.render_list, (spec_id, spec_type)
        )

    def add_query_time(self, view_name: str):
        return self._add_time(lambda: self.run.query_list, (view_name,))

    async def end(self, ping_id: str) -> dict:
        import aiohttp

        assert self.run and self.run.ping_id == ping_id

        pong_perf_counter = get_milliseconds_perf_counter()
        pong_process_time = get_milliseconds_process_time()

        run = self.run
        self.run = None

        if run.profile:
            run.profile.disable()
            run.profile.snapshot_stats()
            profile_bytes = marshal.dumps(run.profile.stats)
            post_blob_url = f"{env.grid_url}/gateway/v2/blob/{env.app_id}/blob"
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    post_blob_url, data=profile_bytes
                )
                blob_id = await response.text()
            profile_blob_url = f"{post_blob_url}/{blob_id}"
        else:
            profile_blob_url = None

        return to_dict(
            LatencyData(
                ping=run.ping_id,
                internal=pong_perf_counter - run.ping_perf_counter,
                process_time=pong_process_time - run.ping_process_time,
                benchmark=run.benchmark,
                profile_blob_url=profile_blob_url,
                render_time=sum(map(lambda item: item[0], run.render_list)),
                render_list=run.render_list,
                query_time=sum(map(lambda item: item[0], run.query_list)),
                query_list=run.query_list,
            )
        )
